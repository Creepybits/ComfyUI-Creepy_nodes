## 🤖 Master Key  
A powerful "Idea Engine" that acts as the creative starting point for generating new and complex prompts.

Philosophy & Use Case
The Master Key is your creative spark plug. It's designed to be the very first step in your prompt generation workflow, providing a clean and focused space to capture your initial idea before it's sent to a powerful AI for expansion. It acts as the "mission briefing" for your AI Art Director.

It's perfect for two main scenarios:

Keyword Expansion: You provide a handful of simple keywords (e.g., "boy, dog, park, red ball"), and the Master Key passes them along to an AI that can weave them into a coherent and detailed scene.

Concept Expansion: You provide a simple sentence describing a scene (e.g., "create a prompt about a boy and a dog playing with a red ball in the park"), and the Master Key feeds this core concept to an AI to be fleshed out with cinematic details, emotional depth, and artistic style.

Inputs
This node has no wired inputs. It is a "start node" where you type your initial idea directly into its text box.

Outputs
text (STRING): The raw text from the input widget, passed through to be used as the prompt for another node (typically the Gemini API node).

Example Workflow
The Master Key is designed to be connected directly to the text or prompt input of an AI node, like the Gemini API node. This allows the AI to take the simple idea from the Master Key and transform it into a rich, detailed final prompt.

<img width="1287" height="420" alt="image" src="https://github.com/user-attachments/assets/8593631b-591f-42fb-8439-110d44bea4d8" />

<img width="1484" height="534" alt="image" src="https://github.com/user-attachments/assets/f5c9b8d5-ca2a-45ad-bc95-21050c6c8b24" />
  


Gemini API: The foundational engine that connects your workflows to Google's AI.

Master Key: Your flagship "Idea Engine" that uses an AI to generate novel concepts from images or text.

Director's Slate: A specialized AI Cinematographer that translates simple ideas into rich, cinematic video prompts.

Art Analyst: An AI art critic that analyzes an image and provides a detailed description or critique.

Gemini Audio Analyzer: An AI sound engineer that listens to audio and generates descriptive text or analysis.

QWEN Prompt: A specialized prompt generator tailored for the Qwen model's unique syntax.

Keyword Extractor: Uses an LLM to intelligently pull out the most important keywords from a block of text.

Audio Keyword Extractor: A specialized version of the above, tailored for transcribed audio.

Categorizer: An AI librarian that reads text and assigns it to a predefined category.

Evaluater Node / People Evaluation Node: AI persona nodes that provide subjective, character-driven evaluations.
