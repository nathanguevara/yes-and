import streamlit as st
from typing import Dict, List, Optional
import uuid
from datetime import datetime
import os
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.frontend.api_client import ComedyAPIClient


def init_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "humor_style" not in st.session_state:
        st.session_state.humor_style = "witty"
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "api_client" not in st.session_state:
        with st.spinner("Connecting to AI Comedy Engine..."):
            try:
                api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
                st.session_state.api_client = ComedyAPIClient(base_url=api_base_url)
                
                # Test connection
                if st.session_state.api_client.is_healthy():
                    st.success("Connected to comedy engine! 🎭")
                else:
                    st.error("Cannot connect to backend API")
                    st.stop()
                    
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
                st.stop()
    
    if "show_metrics" not in st.session_state:
        st.session_state.show_metrics = False
    
    if "awaiting_rating" not in st.session_state:
        st.session_state.awaiting_rating = None


def render_sidebar() -> None:
    """Render the sidebar with controls and information."""
    with st.sidebar:
        st.title("🎭 Comedy Controls")
        
        # Humor style selector
        st.subheader("Humor Style")
        st.session_state.humor_style = st.selectbox(
            "Select your preferred comedy style:",
            ["witty", "sarcastic", "observational", "self-deprecating", "absurd"],
            index=["witty", "sarcastic", "observational", "self-deprecating", "absurd"].index(
                st.session_state.humor_style
            ),
            help="Choose the type of humor you'd like from your AI cohost"
        )
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            st.session_state.show_metrics = st.checkbox(
                "Show Performance Metrics",
                value=st.session_state.show_metrics
            )
            
            if st.button("🔍 Check System Health"):
                health = st.session_state.api_client.health_check()
                if health.get("status") == "healthy":
                    st.success("System is healthy! ✅")
                else:
                    st.error("System issues detected! ❌")
                st.json(health)
        
        # Conversation controls
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.awaiting_rating = None
                st.rerun()
        
        with col2:
            if st.button("🔄 New Session", use_container_width=True):
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.session_state.awaiting_rating = None
                st.rerun()
        
        # Feedback statistics
        st.divider()
        st.subheader("📊 Feedback Stats")
        stats = st.session_state.api_client.get_feedback_stats()
        
        if stats.get("total_ratings", 0) > 0:
            st.metric("Average Rating", f"{stats.get('average_rating', 0):.2f} / 5.0")
            st.metric("Total Ratings", stats.get("total_ratings", 0))
            
            # Style performance
            style_ratings = stats.get("style_ratings", {})
            if style_ratings:
                st.caption("Performance by Style:")
                for style, data in style_ratings.items():
                    if isinstance(data, dict):
                        mean_rating = data.get('mean', 0)
                        count = data.get('count', 0)
                        st.text(f"{style}: {mean_rating:.2f} ⭐ ({count} ratings)")
        else:
            st.info("No ratings yet. Rate responses to see stats!")
        
        # Model info
        with st.expander("🤖 Model Info"):
            model_info = st.session_state.api_client.get_model_info()
            st.json(model_info)


def render_rating_widget(message_index: int) -> None:
    """Render a rating widget for a specific message."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    ratings = [
        (col1, "😴", 1, "Not funny"),
        (col2, "🙂", 2, "Slightly amusing"),
        (col3, "😄", 3, "Pretty good"),
        (col4, "😂", 4, "Very funny"),
        (col5, "🤣", 5, "Hilarious!")
    ]
    
    for col, emoji, rating, label in ratings:
        with col:
            if st.button(f"{emoji}", key=f"rate_{message_index}_{rating}", help=label):
                # Save feedback
                user_msg = st.session_state.messages[message_index - 1]
                ai_msg = st.session_state.messages[message_index]
                
                success = st.session_state.api_client.save_feedback(
                    user_input=user_msg["content"],
                    ai_response=ai_msg["content"],
                    humor_style=ai_msg.get("humor_style", "unknown"),
                    rating=rating,
                    session_id=st.session_state.session_id,
                    additional_data={
                        "enhanced": ai_msg.get("enhanced", False),
                        "generation_time": ai_msg.get("generation_time", 0),
                        "humor_score": ai_msg.get("humor_score", 0)
                    }
                )
                
                st.session_state.awaiting_rating = None
                if success:
                    st.success(f"Thanks for rating! ({rating}/5 ⭐)")
                else:
                    st.warning("Rating saved locally (API unavailable)")
                st.rerun()


def render_chat_interface() -> None:
    """Render the main chat interface."""
    st.title("AI Comedy Cohost 🎭")
    st.caption("Your witty AI partner for humorous conversations!")
    
    # Display conversation history
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Show metrics if enabled
            if st.session_state.show_metrics and message["role"] == "assistant":
                with st.expander("📊 Response Metrics"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Generation Time", f"{message.get('generation_time', 0):.2f}s")
                    with col2:
                        st.metric("Humor Score", f"{message.get('humor_score', 0):.2f}")
                    with col3:
                        st.metric("Enhanced", "Yes" if message.get('enhanced', False) else "No")
            
            # Show rating widget for the message we're waiting to rate
            if (st.session_state.awaiting_rating == i and 
                message["role"] == "assistant"):
                st.caption("How funny was that? Rate this response:")
                render_rating_widget(i)
    
    # Chat input
    if prompt := st.chat_input("Say something to your comedy partner..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Cooking up something funny..."):
                try:
                    # Generate response using the API client
                    response, metadata = st.session_state.api_client.generate_response(
                        user_input=prompt,
                        humor_style=st.session_state.humor_style,
                        conversation_history=st.session_state.messages[:-1],  # Exclude the just-added user message
                        session_id=st.session_state.session_id
                    )
                    
                    # Display the response
                    st.write(response)
                    
                    # Store the message with metadata
                    ai_message = {
                        "role": "assistant",
                        "content": response,
                        "original_response": metadata.get("original_response", response),
                        "humor_style": st.session_state.humor_style,
                        "enhanced": metadata.get("enhanced", False),
                        "generation_time": metadata.get("generation_time", 0),
                        "humor_score": metadata.get("humor_score", 0),
                        "session_id": st.session_state.session_id
                    }
                    
                    st.session_state.messages.append(ai_message)
                    
                    # Set this message as awaiting rating
                    st.session_state.awaiting_rating = len(st.session_state.messages) - 1
                    
                except Exception as e:
                    st.error(f"Oops! Comedy malfunction: {str(e)}")
                    st.info("Check if the backend API is running!")
        
        # Rerun to show the rating widget
        st.rerun()


def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title="AI Comedy Cohost",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Render UI components
    render_sidebar()
    render_chat_interface()
    
    # Footer
    st.divider()
    st.caption(
        "💡 **Pro tip**: Try different humor styles to see how your AI cohost adapts! "
        "Rate responses to help improve the comedy engine."
    )


if __name__ == "__main__":
    main()