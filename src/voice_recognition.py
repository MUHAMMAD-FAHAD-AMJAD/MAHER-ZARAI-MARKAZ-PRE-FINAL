#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import queue
import logging
import threading
import sounddevice as sd
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import pyttsx3

# Set up logging
logger = logging.getLogger('voice')

class VoiceRecognitionManager(QObject):
    """Manager for voice recognition functionality"""
    
    # Define signals
    command_recognized = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Initialize voice recognition manager"""
        super().__init__(parent)
        self.parent = parent
        self.running = False
        self.thread = None
        self.voice_processor = None
        self.tts_engine = None
        
        # Initialize text-to-speech engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            # Set English voice
            for voice in voices:
                if 'english' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        except Exception as e:
            logger.error(f"Error initializing text-to-speech: {e}")
            self.tts_engine = None
        
        # Connect signal to command handler
        self.command_recognized.connect(self.handle_command)
    
    def start(self):
        """Start voice recognition in a separate thread"""
        if self.running:
            return
        
        try:
            # Create voice processor
            self.voice_processor = VoiceProcessor()
            
            # Connect signal
            self.voice_processor.command_recognized.connect(self.on_command_recognized)
            
            # Start thread
            self.thread = QThread()
            self.voice_processor.moveToThread(self.thread)
            self.thread.started.connect(self.voice_processor.start_recognition)
            self.thread.finished.connect(self.voice_processor.stop_recognition)
            
            self.running = True
            self.thread.start()
            
            # Speak confirmation
            self.speak("Voice commands activated")
            
            logger.info("Voice recognition started")
            return True
        
        except Exception as e:
            logger.error(f"Error starting voice recognition: {e}")
            self.running = False
            return False
    
    def stop(self):
        """Stop voice recognition"""
        if not self.running:
            return
        
        try:
            # Speak confirmation
            self.speak("Voice commands deactivated")
            
            # Stop voice processor
            if self.voice_processor:
                self.voice_processor.stop_recognition()
            
            # Stop thread
            if self.thread:
                self.thread.quit()
                self.thread.wait()
            
            self.running = False
            logger.info("Voice recognition stopped")
        
        except Exception as e:
            logger.error(f"Error stopping voice recognition: {e}")
    
    def on_command_recognized(self, command):
        """Handle recognized command from voice processor"""
        logger.info(f"Voice command recognized: {command}")
        self.command_recognized.emit(command)
    
    def speak(self, text):
        """Speak text using text-to-speech engine"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"Text-to-speech error: {e}")
    
    def handle_command(self, command):
        """Process recognized voice command"""
        command = command.lower().strip()
        
        # Check if parent window exists
        if not self.parent:
            return
        
        try:
            # Billing commands
            if "new sale" in command or "start sale" in command:
                self.speak("Starting new sale")
                # Switch to billing tab and clear current sale
                self.parent.tab_widget.setCurrentIndex(0)  # Billing tab
                self.parent.billing_tab.clear_sale()
                
            elif "add product" in command or "add item" in command:
                # Extract product name from command
                parts = command.split("add product")
                if len(parts) > 1:
                    product_name = parts[1].strip()
                    self.speak(f"Adding {product_name}")
                    self.parent.tab_widget.setCurrentIndex(0)  # Billing tab
                    self.parent.billing_tab.search_and_add_product(product_name)
                else:
                    self.speak("Please specify a product name")
            
            elif "complete sale" in command or "finish sale" in command:
                self.speak("Completing sale")
                self.parent.tab_widget.setCurrentIndex(0)  # Billing tab
                self.parent.billing_tab.complete_sale()
            
            # Navigation commands
            elif "go to billing" in command:
                self.speak("Opening billing")
                self.parent.tab_widget.setCurrentIndex(0)
                
            elif "go to inventory" in command:
                self.speak("Opening inventory")
                self.parent.tab_widget.setCurrentIndex(1)
                
            elif "go to customers" in command:
                self.speak("Opening customers")
                self.parent.tab_widget.setCurrentIndex(2)
                
            elif "go to reports" in command and self.parent.user_data['role'] == 'admin':
                self.speak("Opening reports")
                self.parent.tab_widget.setCurrentIndex(3)
                
            elif "go to settings" in command and self.parent.user_data['role'] == 'admin':
                self.speak("Opening settings")
                self.parent.tab_widget.setCurrentIndex(4)
            
            # System commands
            elif "logout" in command:
                self.speak("Logging out")
                self.parent.logout()
                
            elif "exit" in command or "close" in command:
                self.speak("Closing application")
                self.parent.close()
            
            # Help command
            elif "help" in command or "what can i say" in command:
                self.show_voice_help()
            
            else:
                self.speak("Command not recognized")
        
        except Exception as e:
            logger.error(f"Error handling voice command: {e}")
            self.speak("Error processing command")
    
    def show_voice_help(self):
        """Show available voice commands"""
        help_text = (
            "Available voice commands:\n\n"
            "Billing:\n"
            "- New sale / Start sale\n"
            "- Add product [product name]\n"
            "- Complete sale / Finish sale\n\n"
            "Navigation:\n"
            "- Go to billing\n"
            "- Go to inventory\n"
            "- Go to customers\n"
            "- Go to reports (admin only)\n"
            "- Go to settings (admin only)\n\n"
            "System:\n"
            "- Logout\n"
            "- Exit / Close\n"
            "- Help / What can I say"
        )
        
        self.speak("Here are the available voice commands")
        
        # Show help dialog
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self.parent, "Voice Commands Help", help_text)


class VoiceProcessor(QObject):
    """Processor for voice recognition using Vosk"""
    
    # Define signals
    command_recognized = pyqtSignal(str)
    
    def __init__(self):
        """Initialize voice processor"""
        super().__init__()
        self.running = False
        self.q = queue.Queue()
        
        # Try to import vosk
        try:
            from vosk import Model, KaldiRecognizer
            self.vosk_available = True
            self.Model = Model
            self.KaldiRecognizer = KaldiRecognizer
        except ImportError:
            logger.error("Vosk library not found. Voice recognition will not be available.")
            self.vosk_available = False
    
    def start_recognition(self):
        """Start voice recognition"""
        if not self.vosk_available:
            logger.error("Vosk not available. Cannot start voice recognition.")
            return
        
        try:
            # Find model directory
            model_dirs = [
                os.path.join('assets', 'vosk_models', 'vosk-model-small-en-us-0.15'),
                os.path.join('assets', 'vosk_models', 'en-us'),
                os.path.join('assets', 'vosk_models')
            ]
            
            model_path = None
            for path in model_dirs:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if not model_path:
                logger.error("Vosk model not found. Cannot start voice recognition.")
                return
            
            # Load model
            model = self.Model(model_path)
            
            # Set up audio parameters
            device_info = sd.query_devices(None, 'input')
            samplerate = int(device_info['default_samplerate'])
            
            # Create recognizer
            self.recognizer = self.KaldiRecognizer(model, samplerate)
            self.recognizer.SetWords(True)
            
            # Start audio stream
            self.running = True
            
            def audio_callback(indata, frames, time, status):
                """Callback for audio stream"""
                if status:
                    logger.warning(f"Audio status: {status}")
                if self.running:
                    self.q.put(bytes(indata))
            
            # Start audio stream
            self.stream = sd.RawInputStream(
                samplerate=samplerate,
                blocksize=8000,
                device=None,
                dtype='int16',
                channels=1,
                callback=audio_callback
            )
            
            with self.stream:
                logger.info("Voice recognition listening...")
                
                while self.running:
                    # Process audio data
                    data = self.q.get()
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get('text', '')
                        
                        if text:
                            # Emit signal with recognized command
                            self.command_recognized.emit(text)
        
        except Exception as e:
            logger.error(f"Error in voice recognition: {e}")
            self.running = False
    
    def stop_recognition(self):
        """Stop voice recognition"""
        self.running = False
        
        # Clear queue
        while not self.q.empty():
            self.q.get_nowait()


# Test function
def test_voice_recognition():
    """Test voice recognition functionality"""
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
    
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Voice Recognition Test")
            self.setGeometry(100, 100, 400, 300)
            
            # Create central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Create layout
            layout = QVBoxLayout()
            central_widget.setLayout(layout)
            
            # Create status label
            self.status_label = QLabel("Voice recognition not active")
            layout.addWidget(self.status_label)
            
            # Create command label
            self.command_label = QLabel("No command recognized")
            layout.addWidget(self.command_label)
            
            # Create start button
            start_button = QPushButton("Start Voice Recognition")
            start_button.clicked.connect(self.start_voice)
            layout.addWidget(start_button)
            
            # Create stop button
            stop_button = QPushButton("Stop Voice Recognition")
            stop_button.clicked.connect(self.stop_voice)
            layout.addWidget(stop_button)
            
            # Create voice recognition manager
            self.voice_manager = None
        
        def start_voice(self):
            """Start voice recognition"""
            if not self.voice_manager:
                self.voice_manager = VoiceRecognitionManager(self)
                self.voice_manager.command_recognized.connect(self.on_command)
            
            if self.voice_manager.start():
                self.status_label.setText("Voice recognition active")
        
        def stop_voice(self):
            """Stop voice recognition"""
            if self.voice_manager:
                self.voice_manager.stop()
                self.status_label.setText("Voice recognition stopped")
        
        def on_command(self, command):
            """Handle recognized command"""
            self.command_label.setText(f"Command: {command}")
    
    # Create application
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Set up logging for standalone test
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run test
    test_voice_recognition() 