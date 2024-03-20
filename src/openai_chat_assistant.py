"""
Author: Temiloluwa Adeoti
Date: 20.03.2024
Email: temmiecvml@gmail.com

This module provides a simple AI assistant and message classes for managing conversations.

Example usage:

Default settings usage:
    assistant_default = Assistant()
    assistant_default.chat("what is the best way to impress your girlfriend")
    assistant_default.chat("what if she doesn't like to feel special?")

Custom settings usage:
    system_message = "You are a helpful assistant that always responds with 'heck ya!'"
    chat_config = {"model": "gpt-3.5-turbo", "temperature": 0.7, "max_tokens": 100}

    assistant = Assistant(system_message, chat_config)
    assistant.chat("what is the best way to impress your girlfriend")
    assistant.chat("I don't like your feedback")

Print conversation history:
    print(assistant.convo_history)
"""

from typing import List, Dict
from datetime import datetime
import pytz
import os 


class Message:
    """A class representing a message in a conversation."""
    __slots__ = ['role', 'content', 'timestamp']
    
    def __init__(self, role: str = "User", content: str = "", timestamp: str = None):
        """Initialize a Message object.
        
        Args:
            role (str): The role of the message sender. Default is "User".
            content (str): The content of the message. Default is an empty string.
            timestamp (str): The timestamp of the message in "%Y-%m-%d %H:%M:%S" format.
                If not provided, the current time in the Europe/Berlin timezone will be used.
        """
        self.role = role
        self.content = content
        if timestamp:
            self.timestamp = timestamp
        else:
            berlin_timezone = pytz.timezone('Europe/Berlin')
            berlin_time = datetime.now(berlin_timezone)
            self.timestamp = berlin_time.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self) -> str:
        """Return a string representation of the Message object."""
        return f"Message(role='{self.role}', content='{self.content}', timestamp='{self.timestamp}')"

    def prep(self) -> Dict[str, str]:
        """Prepare the message for sending.
        
        Returns:
            dict: A dictionary containing the role and content of the message.
        """
        return {"role": self.role, "content": self.content}


class Assistant:
    """A class representing an AI assistant."""
    
    def __init__(self,  system_message: str = "", 
                        chat_config: Dict[str, str] = {},
                        api_key_path: str = ""):
        """Initialize an Assistant object.
        
        Args:
            system_message (str): The initial system message. Default is an empty string.
            chat_config (dict): Configuration settings for the chat. Default is an empty dictionary.
            api_key_path (str): The path to the OpenAI API key file. If not provided, 
                it will try to read the key from the environment variable "OPENAI_API_KEY".
        
        Raises:
            ValueError: If the OpenAI API key is not supplied.
        """
        if not api_key_path:
            try:
                api_key_path = os.environ["OPENAI_API_KEY"]
            except KeyError:
                raise ValueError("OpenAI API key not supplied")

        self.client = OpenAI(api_key=api_key_path)
        self.convo_history: List[Message] = []
        self._init_assistant(system_message, chat_config) 


    def _init_assistant(self, system_message: str = "", 
                        chat_config: Dict[str, str] = {}): 
        """Initialize the assistant.
        
        Args:
            system_message (str): The initial system message. If not provided, 
                a default system message will be used.
            chat_config (dict): Configuration settings for the chat. Default is an empty dictionary.
        """
        if not system_message:
            system_message = "You are a helpful assistant."
            print(f"Using default system message: {system_message}")  
        
        self.convo_history.append(Message(role="system", content=system_message))
        self.chat_config = {"model": "gpt-3.5-turbo"}

    def _continue_convo(self, user_message: str) -> List[Message]:  
        """Continue the conversation with a user message.
        
        Args:
            user_message (str): The message sent by the user.
        
        Returns:
            list: The updated conversation history.
        
        Raises:
            ValueError: If the conversation history has not started.
        """
        if not self.convo_history:
            raise ValueError("Conversation history should have started")
        self.convo_history.append(Message(role="user", content=user_message))
        return self.convo_history

    def configure_convo(self, chat_config: Dict[str, str]) -> None:
        """Configure the conversation settings.
        
        Args:
            chat_config (dict): Configuration settings for the chat.
        """
        self.chat_config = chat_config

    def prep_history(self, summarize_history: bool = False) -> List[Dict[str, str]]:
        """Prepare the conversation history for sending.
        
        Args:
            summarize_history (bool): Whether to summarize the conversation history. Default is False.
        
        Returns:
            list: A list of dictionaries containing the role and content of each message.
        """
        messages = [message.prep() for message in self.convo_history]
        if summarize_history:
            pass  # Placeholder for summarization logic
        return messages
    
    def chat(self, user_message: str) -> str:
        """Chat with the assistant.
        
        Args:
            user_message (str): The message sent by the user.
        
        Returns:
            str: The response from the assistant.
        
        Raises:
            ValueError: If no user message input is provided.
        """
        if not user_message:
            raise ValueError("No User message input")
        
        self._continue_convo(user_message)
        messages = self.prep_history()
        completion = self.client.chat.completions.create(**self.chat_config, messages=messages)
        response = completion.choices[0].message.content
        
        self.convo_history.append(Message(role="assistant", content=response))
        
        return self.convo_history[-1].content
