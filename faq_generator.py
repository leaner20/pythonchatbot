# faq_generator.py
import re
from typing import List, Dict


def generate_faqs(text: str, max_faqs: int = 5) -> List[Dict[str, str]]:
    """
    Generate FAQs from text with improved logic
    Args:
        text: Input text to analyze
        max_faqs: Maximum number of FAQs to return
    Returns:
        List of dictionaries with 'question' and 'answer' keys
    """
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")

        # Pre-process text
        text = re.sub(r'\s+', ' ', text).strip()[:10000]  # Limit to 10k chars

        # Enhanced mock FAQ generation
        contact_match = re.search(r'contact\s+(us|support)?@?\b', text, re.I)
        services_match = re.search(r'(offer|provide|sell)\s+([^.]+)', text, re.I)

        base_faqs = [
            {
                "question": "How do I contact support?",
                "answer": "Visit our Contact Us page." if contact_match
                else "Please check the website footer for contact details."
            },
            {
                "question": "What services do you offer?",
                "answer": f"We specialize in {services_match.group(2).strip()}." if services_match
                else "We provide technology solutions across multiple domains."
            },
            {
                "question": "Where are you located?",
                "answer": "Our headquarters is in Bengaluru, India."
            }
        ]

        # Ensure we don't exceed requested max FAQs
        return base_faqs[:min(max_faqs, len(base_faqs))]

    except Exception as e:
        print(f"⚠️ FAQ Generation Error: {str(e)}")
        # Return safe default FAQs if error occurs
        return [
            {
                "question": "How can I get help?",
                "answer": "Please contact our support team."
            }
        ]


# Improved test cases
if __name__ == "__main__":
    test_cases = [
        ("We sell AI chatbots. Contact at support@company.com", 3),
        ("", 2),  # Empty string test
        (123, 2),  # Invalid input test
        ("Specializing in cloud computing and data analytics", 1)
    ]

    for text, max_f in test_cases:
        print(f"\nInput: {text}")
        try:
            faqs = generate_faqs(text, max_f)
            print(f"Generated {len(faqs)} FAQs:")
            for i, faq in enumerate(faqs, 1):
                print(f"{i}. Q: {faq['question']}")
                print(f"   A: {faq['answer']}")
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
