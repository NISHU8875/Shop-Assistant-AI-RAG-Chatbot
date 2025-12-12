from semantic_router import Route
# from semantic_router.routers import SemanticRouter
from semantic_router.layer import RouteLayer  # Changed from semantic_router.routers
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "Is cash on delivery available?",
        "Do you accept online payments?",
        "What are your shipping charges?",
        "How do I cancel my order?",
        "What is your refund policy?",
        "Do you offer EMI options?",
        "Can I pay with UPI?",
        "What cards do you accept?",
        "How long does delivery take?",
        "What if I receive a defective product?",
        "Can I exchange a product?",
        "Do you ship internationally?",
        "What are your business hours?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
        "Show me all nike shoes below Rs. 5000",
        "Give me highly rated shoes",
        "List all products with discount above 30%",
        "Show me running shoes for women",
        "What are the cheapest shoes available?",
        "Display all Adidas products",
        "Show products with rating above 4",
        "Give me shoes in the price range 2000 to 5000",
    ]
)

chitchat = Route(
    name='chitchat',
    utterances=[
        "Hello, how are you?",
        "Hi, I'm Pankaj",
        "What's your name?",
        "Tell me a joke",
        "What's the weather like today?",
        "What is today's date?",
        "Can you help me with fashion advice?",
        "What should I wear for a wedding?",
        "I'm feeling stressed, any suggestions?",
        "How can I improve my style?",
        "What colors go well together?",
        "Tell me about yourself",
        "Good morning",
        "Thank you",
        "How's your day going?",
        "What are some fashion trends?",
        "Can you suggest an outfit?",
        "I need wellness tips",
        "How to stay healthy?",
    ]
)

# Create router without routes first
router = RouteLayer(encoder=encoder)

# Add routes one by one (this builds the index automatically)
router.add(faq)
router.add(sql)
router.add(chitchat)


if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 1000 to 5000").name)
    print(router("Hi, I'm John").name)
    print(router("What should I wear today?").name)

