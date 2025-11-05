# --- ENV Messages ---
MISSING_ENV_VARS_ERROR = (
    "\n🚨 Missing required environment variables:\n"
    "{vars}\n"
    "➡️ Please add them to your .env file before running the project.\n"
    "Example:\n"
    "OPENAI_API_KEY=your_openai_api_key_here\n"
    "LINKEDIN_ACCESS_TOKEN=your_access_token_here\n"
    "LINKEDIN_PERSON_URN=urn:li:person:xxxxxx\n"
    "POST_NICHE=AI, Technology, Automation\n"
    "GEMINI_API_KEY=your_gemini_api_key_here\n"
)

# --- MongoDB Messages ---
POST_SAVE_ERROR = "🚨 Failed to save post to MongoDB: {error}"
POST_RETRIEVE_ERROR = "🚨 Failed to retrieve posts from MongoDB: {error}"

# --- LinkedIn Messages ---
LINKEDIN_MISSING_CREDENTIALS = "❌ LinkedIn credentials missing (ACCESS_TOKEN or PERSON_URN)."
LINKEDIN_ASSET_REGISTER_FAIL = "❌ Failed to register asset upload: {error}"
LINKEDIN_ASSET_UPLOAD_FAIL = "❌ Failed to upload image to LinkedIn: {error}"
LINKEDIN_POST_SUCCESS = "✅ Post published successfully on LinkedIn."
LINKEDIN_POST_FAIL = "❌ LinkedIn post failed with status {status}: {error}"
LINKEDIN_NETWORK_ERROR = "🌐 Network error during LinkedIn operation: {error}"
REGISTER_UPLOAD_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"
LINKEDIN_POST_API_URL = "https://api.linkedin.com/v2/ugcPosts"

# --- Gemini Messages ---
GEMINI_CLIENT_INIT_FAIL = "❌ Failed to initialize Gemini client: {error}"
GEMINI_IMAGE_GEN_FAIL = "❌ Gemini image generation failed: {error}"
GEMINI_NO_IMAGE_DATA = "⚠️ No image data returned by Gemini. Skipping image upload."
GEMINI_IMAGE_SAVE_FAIL = "❌ Error saving Gemini image locally: {error}"

# --- General ---
TEMP_FILE_REMOVED = "🧹 Temporary image file removed."
OPERATION_SUCCESS = "✅ Operation completed successfully."

# Topic generation
TOPIC_GENERATOR_SYSTEM_PROMPT = (
    "You are a content strategist specialized in LinkedIn posts. "
    "Generate a unique, actionable topic for the given niche. "
    "Return ONLY the title, no additional explanation."
)
TOPIC_GENERATOR_USER_PROMPT = "Generate a unique, actionable topic for the niche: {niche}"

# Content creation
CONTENT_CREATOR_SYSTEM_PROMPT = (
    "You are a professional LinkedIn content writer. "
    "Produce a concise, engaging post with relevant hashtags. "
    "Focus on readability and actionable insights. "
    "Return the post draft ONLY, without any extra commentary."
)
CONTENT_CREATOR_USER_PROMPT = "Create a LinkedIn post draft for: {topic}"

# Reviewer
REVIEWER_SYSTEM_PROMPT = (
    "You are a strict LinkedIn post reviewer. "
    "If the draft is perfect, return EXACTLY 'APPROVED'. "
    "Otherwise, provide a concise critique with actionable improvements. "
    "Do not include the original post content in the critique."
)

# Image generation
IMAGE_GENERATION_INSTRUCTION = (
    "Generate an AI image that visually represents the content or theme of the LinkedIn post. "
    "Return a LinkedIn-compatible asset URN only if generation succeeds."
)

# Post execution
POST_EXECUTOR_FAILURE_MESSAGE = "No final_post available to publish or post failed."
POST_EXECUTOR_SUCCESS_MESSAGE = "LinkedIn post succeeded and saved to MongoDB."

GEMINI_MODEL = "gemini-2.0-flash"

# Logging & error messages
GEMINI_CLIENT_INIT_FAIL = "❌ Failed to initialize Gemini client: {error}"
GEMINI_IMAGE_GEN_FAIL = "❌ Gemini image generation failed: {error}"
GEMINI_NO_IMAGE_DATA = "⚠️ No image data returned by Gemini."
GEMINI_IMAGE_SAVE_FAIL = "❌ Failed to save Gemini image: {error}"
TEMP_FILE_REMOVED = "🗑️ Temporary image file removed."

# Image prompt template
GEMINI_IMAGE_PROMPT_TEMPLATE = (
    "Generate a professional, clean, high-resolution LinkedIn mind map image. "
    "Topic: {topic}"
)