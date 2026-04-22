# KZTaxChecker - IT4IT Product Lifecycle Reflection

## Strategy to Portfolio (S2P)

KZTaxChecker was created to solve a real business problem in Kazakhstan. Many small and medium-sized enterprises (SMEs) regularly submit ESF (electronic invoice) documents, but even minor mistakes in these invoices can lead to significant penalties. Depending on the violation, fines may range from 50 to 200 MRP, which creates financial risk for companies that may not have dedicated tax compliance staff.

The core opportunity was to reduce manual verification work through artificial intelligence. Traditionally, accounting staff or business owners must manually inspect invoice fields such as BIN, VAT rates, dates, and totals. This process can take approximately 5 to 10 hours per week for active businesses. KZTaxChecker reduces this task to around 30 seconds by automatically scanning uploaded files and highlighting risks instantly.

From an investment perspective, the business justification is strong. Preventing only one tax fine can fully justify the time and resources spent building the tool. Therefore, the project demonstrates a clear return on investment while also improving operational efficiency.

## Requirement to Deploy (R2D)

My role in this project was as the architect rather than the programmer. Instead of writing code manually, I designed the product concept, selected the technology stack, defined the required features, and coordinated development through AI-assisted prompting.

I directed the AI agent through multiple development sessions and iterative prompts to gradually improve the application. Each session focused on one part of the product lifecycle: initial setup, file processing, validation logic, UI design, and deployment readiness.

One of the hardest challenges was file extraction quality. Early versions of the generated solution used libraries that handled PDF text poorly, especially for Cyrillic characters commonly used in Kazakhstan invoices. This caused unreadable output and inaccurate analysis. I solved this by explicitly redirecting development toward `pdfplumber`, which provided more reliable text extraction.

Another challenge was implementing Kazakhstan-specific validation logic such as BIN checksum rules and tax compliance checks. Generic AI outputs often lacked local regulatory accuracy, so I had to refine prompts several times until the logic aligned with the intended requirements.

## Request to Fulfill (R2F)

The final delivery model was a Streamlit-based web application. This was selected because it allows rapid development, simple deployment, and a clean user interface without requiring heavy frontend engineering.

The user journey is straightforward:

Upload PDF or TXT invoice file → Click Analyze → Receive color-coded risk report → Download JSON report.

The interface uses clear visual signals. High-risk issues appear in red, medium-risk warnings in yellow, and successful checks in green. This allows users to understand results immediately without reading technical logs.

Accessibility was also considered. The solution runs locally on a normal laptop, requires no expensive infrastructure, and can operate using a free Gemini API key. This lowers adoption barriers for students, freelancers, and SMEs.

## Detect to Correct (D2C)

Operational monitoring is an important part of any digital product. For KZTaxChecker, a future-ready logging model includes a `logs.json` file to track API requests, timestamps, and outcomes. This can help identify usage trends, failures, and abnormal behavior.

Cost control was addressed through the use of Gemini’s free tier, which supports approximately 60 requests per minute. For early-stage usage and testing, this is sufficient and avoids immediate cloud costs.

Because AI systems may occasionally misclassify results, hallucination handling is necessary. A planned enhancement is a “Report false error” button so users can flag incorrect findings. This would create a feedback loop for continuous improvement.

Error handling is also included through try-catch mechanisms for API timeouts, invalid files, or malformed responses. This ensures the tool fails gracefully rather than crashing during use.

## Reflection on Agentic Development

The easiest part of development was generating boilerplate code. The AI agent quickly produced Streamlit layouts, file upload logic, JSON export functions, and basic validation structures that would normally take much longer to build manually.

The hardest part was converting vague requirements into precise instructions. For example, explaining the BIN checksum algorithm and Kazakhstan-specific tax rules required several prompt iterations before the output was correct. This showed that AI can generate code quickly, but only when guided with clear architecture and domain logic.

The biggest lesson I learned is that architecture matters more than syntax. Writing lines of code is no longer the main bottleneck. The more valuable skill is defining the right system, workflows, validations, and user outcomes. In this project, success depended less on programming and more on product thinking, problem framing, and iterative decision-making.

Overall, KZTaxChecker demonstrated how an architect can use AI agents productively to deliver a practical compliance solution with real business value.
