from dotenv import load_dotenv
load_dotenv()

import gradio as gr
from elevenlabs import ElevenLabs
from blog_summarizer import *

def process_url(url):
    try: 
        # Get summary from blog summarizer 
        summary = run_blog_summary_crew(url)

        # Convert summary to speech using Elevenlabs
        client = ElevenLabs()
        response = client.text_to_speech.convert(
            voice_id="JBFqnCBsd6RMkjVDRZzb", 
            output_format="mp3_44100_128", 
            text=summary[:350], 
            model_id="eleven_flash_v2_5"
        )
        
        audio_path = "output.mp3"
        with open(audio_path, "wb") as f:
            for chunk in response:
                f.write(chunk)
                               
        return summary, audio_path, "Podcast generated successfully"
    
    except Exception as e:
        print("Error Processing URL: ", str(e))
        return None, None, f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# AI Podcast Generator")
    gr.Markdown("Enter a blog URL to generate a podcast episode from its content.")
    
    with gr.Row():
        url = gr.Textbox(label="Blog URL", placeholder="https://example.com/blog-post")
        
    generate_btn = gr.Button("Generate Podcast")
    status = gr.Textbox(label="Status", lines=1)
    
    with gr.Row():
        summary_output = gr.Textbox(label="Blog Summary", lines=17)

    with gr.Row():
        audio_output = gr.Audio(label="Podcast Audio")
        
    generate_btn.click(
        fn=process_url, 
        inputs=[url],
        outputs=[summary_output, audio_output, status]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme="soft") 
    

