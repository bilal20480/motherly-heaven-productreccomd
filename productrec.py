import streamlit as st
import requests
import json
from typing import List, Dict, Optional, Tuple
import os
import base64

st.set_page_config(
        page_title="Motherly Heaven", 
        page_icon="🤱", 
        layout="wide"
    )

# Load background image and convert to base64
def get_base64_image():
    for ext in ["webp", "jpg", "jpeg", "png"]:
        image_path = f"bg1.{ext}"
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

bg_img = get_base64_image()

# Inject custom background CSS
if bg_img:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.5)),
                        url("data:image/png;base64,{bg_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 248, 243, 0.45);
            padding: 2rem 3rem;
            border-radius: 18px;
            margin-top: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #4B4B4B;
            font-family: 'Segoe UI', sans-serif;
        }}
        .export-buttons {{
            margin-top: 20px;
        }}
        
        /* Custom sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: #e4c3df !important;
        }}
        [data-testid="stSidebar"] .stRadio label, 
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stTextInput label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stHeader {{
            color: #5c3b5e !important;
        }}
        [data-testid="stSidebar"] .stRadio div div div div {{
            background-color: #f3e0f2 !important;
        }}
        [data-testid="stSidebar"] .stSelectbox select,
        [data-testid="stSidebar"] .stTextInput input,
        [data-testid="stSidebar"] .stSlider div div div div {{
            background-color: #f3e0f2 !important;
            color: #5c3b5e !important;
            border-color: #d5b4cf !important;
        }}
        [data-testid="stSidebar"] .stButton button {{
            background-color: #b36fa0 !important;
            color: white !important;
            border: none !important;
        }}
        [data-testid="stSidebar"] .stButton button:hover {{
            background-color: #a14c86 !important;
        }}
        [data-testid="stSidebar"] .stHeader h3 {{
            color: #a14c86 !important;
        }}
        </style>
    """, unsafe_allow_html=True)
# --- Configuration ---
# Store these in your Streamlit secrets (secrets.toml)
API_KEY = st.secrets.get("google_api", {}).get("key", "AIzaSyBYhKY9MQgCDX__BoKqvqx6z30VlnIAdsA")
CSE_ID = st.secrets.get("google_api", {}).get("cse_id", "6517142dafb7440d8")

# --- Product Database (Trimmed for brevity) ---
MOTHER_PRODUCTS = {
    "1st Trimester": [
        {"name": "Prenatal Vitamins", "desc": "Essential vitamins for early pregnancy development"},
        {"name": "Ginger Chews", "desc": "For relieving morning sickness and nausea"},
        {"name": "Pregnancy Journal", "desc": "To document your pregnancy journey"},
        {"name": "Body Pillow", "desc": "For better sleep during early pregnancy"},
        {"name": "Stretch Mark Cream", "desc": "Early prevention of stretch marks"},
        {"name": "Hydration Tracker", "desc": "To ensure proper water intake"},
        {"name": "Compression Socks", "desc": "For improving circulation"},
        {"name": "Pregnancy Books", "desc": "Educational resources for expecting moms"},
        {"name": "Sea Bands", "desc": "Acupressure bands for nausea relief"},
        {"name": "Electrolyte Supplements", "desc": "For hydration and mineral balance"},
        {"name": "Maternity Bras", "desc": "Comfortable bras for changing body"},
        {"name": "Pregnancy App Subscription", "desc": "Weekly pregnancy updates"},
        {"name": "Belly Butter", "desc": "For moisturizing growing belly"},
        {"name": "Prenatal Yoga Mat", "desc": "For safe pregnancy exercises"},
        {"name": "Heartburn Relief", "desc": "Safe antacids for pregnancy"},
        {"name": "Pregnancy Pillow", "desc": "Full body support for sleeping"},
        {"name": "Folic Acid Supplements", "desc": "Essential for fetal development"},
        {"name": "Maternity Leggings", "desc": "Comfortable stretchy bottoms"},
        {"name": "Water Bottle with Timer", "desc": "Track daily water intake"},
        {"name": "Pregnancy Tea", "desc": "Caffeine-free herbal teas"},
        {"name": "Nipple Cream", "desc": "Early preparation for breastfeeding"},
        {"name": "Prenatal Massage Oil", "desc": "For relaxation and skin care"},
        {"name": "Pregnancy Safe Skincare", "desc": "Chemical-free beauty products"},
        {"name": "Belly Band", "desc": "Support for growing belly"},
        {"name": "Pregnancy Safe Sunscreen", "desc": "Protection for sensitive skin"}
    ],
    "2nd Trimester": [
        {"name": "Maternity Jeans", "desc": "Comfortable pants with belly panel"},
        {"name": "Fetal Doppler", "desc": "To listen to baby's heartbeat at home"},
        {"name": "Belly Support Band", "desc": "For back and belly support"},
        {"name": "Pregnancy Belt", "desc": "Support for growing bump"},
        {"name": "Maternity Swimwear", "desc": "For pool exercises and comfort"},
        {"name": "Pregnancy Wedge Pillow", "desc": "Targeted belly support"},
        {"name": "Baby Kicks Counter", "desc": "Track baby's movement patterns"},
        {"name": "Maternity Dress", "desc": "Stylish and comfortable outfits"},
        {"name": "Prenatal Classes", "desc": "Online or in-person education"},
        {"name": "Belly Cast Kit", "desc": "To preserve your baby bump"},
        {"name": "Pregnancy Photoshoot Props", "desc": "For maternity photos"},
        {"name": "Nursing Pads", "desc": "Early preparation for breastfeeding"},
        {"name": "Breast Pump", "desc": "Researching and selecting options"},
        {"name": "Baby Name Book", "desc": "Inspiration for naming your baby"},
        {"name": "Maternity Nightgown", "desc": "Comfortable sleepwear"},
        {"name": "Pregnancy Safe Hair Dye", "desc": "For coloring hair safely"},
        {"name": "Belly Oil", "desc": "For moisturizing and preventing stretch marks"},
        {"name": "Pregnancy Ball", "desc": "For exercise and labor preparation"},
        {"name": "Maternity Underwear", "desc": "Comfortable panties for bump"},
        {"name": "Pregnancy Journal", "desc": "Documenting milestones"},
        {"name": "Baby Registry", "desc": "Start planning baby essentials"},
        {"name": "Maternity Jacket", "desc": "For changing body shape"},
        {"name": "Pregnancy Safe Makeup", "desc": "Non-toxic beauty products"},
        {"name": "Nursing Bras", "desc": "Preparing for postpartum"},
        {"name": "Childbirth Books", "desc": "Education about labor and delivery"}
    ],
    "3rd Trimester": [
        {"name": "Hospital Bag", "desc": "For packing labor essentials"},
        {"name": "Nursing Pillow", "desc": "For breastfeeding support"},
        {"name": "Perineal Massage Oil", "desc": "Preparation for childbirth"},
        {"name": "Postpartum Underwear", "desc": "Comfortable high-waisted panties"},
        {"name": "Maternity Robe", "desc": "For hospital and postpartum comfort"},
        {"name": "Breastfeeding Cover", "desc": "For nursing in public"},
        {"name": "Labor Playlist", "desc": "Music for relaxation during labor"},
        {"name": "Nipple Shield", "desc": "For breastfeeding assistance"},
        {"name": "Postpartum Pads", "desc": "Heavy flow pads for recovery"},
        {"name": "Sitz Bath", "desc": "For postpartum healing"},
        {"name": "Nursing Nightgown", "desc": "Easy access for breastfeeding"},
        {"name": "Baby Memory Book", "desc": "To record first moments"},
        {"name": "Milk Storage Bags", "desc": "For freezing breastmilk"},
        {"name": "Perineal Cold Packs", "desc": "Postpartum pain relief"},
        {"name": "Nursing Tank Tops", "desc": "Easy breastfeeding access"},
        {"name": "Diaper Bag", "desc": "For carrying baby essentials"},
        {"name": "Baby Swaddle Blankets", "desc": "For newborn comfort"},
        {"name": "Postpartum Belly Wrap", "desc": "For abdominal support"},
        {"name": "Breastfeeding App", "desc": "Track feeding and diapers"},
        {"name": "Baby Book", "desc": "For tracking growth and milestones"},
        {"name": "Nursing Cover", "desc": "For discreet breastfeeding"},
        {"name": "Postpartum Herbs", "desc": "For healing and milk supply"},
        {"name": "Baby Carrier", "desc": "Hands-free baby wearing"},
        {"name": "Postpartum Vitamins", "desc": "Continued nutrition after birth"},
        {"name": "Baby First Aid Kit", "desc": "Essential medical supplies"}
    ],
    "Postpartum": [
        {"name": "Nursing Pads", "desc": "For breast leakage protection"},
        {"name": "Perineal Spray", "desc": "For postpartum pain relief"},
        {"name": "Postpartum Belly Band", "desc": "For abdominal support"},
        {"name": "Nipple Cream", "desc": "For sore breastfeeding nipples"},
        {"name": "Sitz Bath Soak", "desc": "For healing after delivery"},
        {"name": "Postpartum Underwear", "desc": "Comfortable high-waisted"},
        {"name": "Breast Pump", "desc": "For expressing milk"},
        {"name": "Milk Storage Bags", "desc": "For freezing breastmilk"},
        {"name": "Nursing Bras", "desc": "Easy access for breastfeeding"},
        {"name": "Postpartum Tea", "desc": "For relaxation and milk supply"},
        {"name": "Heating Pad", "desc": "For afterpains relief"},
        {"name": "Stool Softener", "desc": "For postpartum bowel movements"},
        {"name": "Nursing Cover", "desc": "For discreet breastfeeding"},
        {"name": "Postpartum Vitamins", "desc": "Continued nutrition"},
        {"name": "Perineal Cold Packs", "desc": "For swelling and pain"},
        {"name": "Nursing Tank Tops", "desc": "Easy breastfeeding access"},
        {"name": "Breastfeeding Pillow", "desc": "For comfortable nursing"},
        {"name": "Postpartum Journal", "desc": "To document recovery"},
        {"name": "Hands-Free Pumping Bra", "desc": "For multitasking"},
        {"name": "Postpartum Cookbook", "desc": "Healing meal recipes"},
        {"name": "Baby Wrap Carrier", "desc": "For keeping baby close"},
        {"name": "Postpartum Yoga DVD", "desc": "Gentle exercises"},
        {"name": "Lactation Cookies", "desc": "For boosting milk supply"},
        {"name": "Postpartum Essential Oils", "desc": "For relaxation"},
        {"name": "Nipple Shields", "desc": "For breastfeeding assistance"}
    ]
}

BABY_PRODUCTS  = {
    "0-3 months": [
        {"name": "Newborn Diapers", "desc": "Size NB for tiny babies"},
        {"name": "Baby Wipes", "desc": "Fragrance-free for sensitive skin"},
        {"name": "Onesies", "desc": "Simple snap-front bodysuits"},
        {"name": "Swaddle Blankets", "desc": "For secure wrapping"},
        {"name": "Bassinet", "desc": "Safe sleeping space"},
        {"name": "Baby Bottles", "desc": "Small size for newborns"},
        {"name": "Pacifiers", "desc": "Newborn appropriate size"},
        {"name": "Baby Nail Clippers", "desc": "Safe for tiny nails"},
        {"name": "Infant Car Seat", "desc": "Rear-facing for safety"},
        {"name": "Baby Bathtub", "desc": "For safe bathing"},
        {"name": "Burp Cloths", "desc": "For spit-up protection"},
        {"name": "Baby Monitor", "desc": "To watch sleeping baby"},
        {"name": "Diaper Rash Cream", "desc": "For prevention and treatment"},
        {"name": "Baby Carrier", "desc": "For keeping baby close"},
        {"name": "White Noise Machine", "desc": "For better sleep"},
        {"name": "Baby Swing", "desc": "Soothing motion"},
        {"name": "Nasal Aspirator", "desc": "For clearing stuffy nose"},
        {"name": "Baby Towels", "desc": "Soft and absorbent"},
        {"name": "Baby Wash", "desc": "Gentle cleanser"},
        {"name": "Baby Lotion", "desc": "For delicate skin"},
        {"name": "Baby Hat", "desc": "For temperature regulation"},
        {"name": "Mittens", "desc": "Prevent face scratching"},
        {"name": "Baby Socks", "desc": "Keep feet warm"},
        {"name": "Diaper Bag", "desc": "For carrying essentials"},
        {"name": "Baby Book", "desc": "For tracking milestones"}
    ],
    "3-6 months": [
        {"name": "Size 1 Diapers", "desc": "For growing babies"},
        {"name": "Teething Toys", "desc": "For sore gums"},
        {"name": "Activity Gym", "desc": "For tummy time"},
        {"name": "Baby Bouncer", "desc": "Entertainment seat"},
        {"name": "Sleep Sack", "desc": "Safe wearable blanket"},
        {"name": "Baby Food Maker", "desc": "Preparing for solids"},
        {"name": "High Chair", "desc": "For upcoming meals"},
        {"name": "Baby Spoons", "desc": "Soft-tip for first foods"},
        {"name": "Bibs", "desc": "For drool and spills"},
        {"name": "Baby Books", "desc": "Board books for reading"},
        {"name": "Rattles", "desc": "Sensory toys"},
        {"name": "Baby Jumper", "desc": "For active play"},
        {"name": "Sippy Cups", "desc": "Transition from bottles"},
        {"name": "Baby Sunhat", "desc": "Sun protection"},
        {"name": "Baby Sunscreen", "desc": "Safe for infants"},
        {"name": "Convertible Car Seat", "desc": "Grows with baby"},
        {"name": "Baby Gate", "desc": "For safety as they move"},
        {"name": "Soft Blocks", "desc": "For early play"},
        {"name": "Baby Mirror", "desc": "For self-discovery"},
        {"name": "Stacking Rings", "desc": "Developmental toy"},
        {"name": "Baby Leggings", "desc": "Comfortable movement"},
        {"name": "Drool Pads", "desc": "For crib and carrier"},
        {"name": "Baby Shoes", "desc": "Soft-soled first shoes"},
        {"name": "Teething Necklace", "desc": "For nursing moms"},
        {"name": "Baby Toothbrush", "desc": "Early oral care"}
    ],
    "6-9 months": [
        {"name": "Size 2 Diapers", "desc": "For active babies"},
        {"name": "Baby Bowls", "desc": "For first foods"},
        {"name": "Sippy Cups", "desc": "Transition from bottles"},
        {"name": "Baby Food Storage", "desc": "For homemade purees"},
        {"name": "Crawling Mat", "desc": "Soft play surface"},
        {"name": "Baby Walker", "desc": "For assisted movement"},
        {"name": "Stacking Toys", "desc": "Developmental play"},
        {"name": "Board Books", "desc": "Durable for babies"},
        {"name": "Bath Toys", "desc": "For water play"},
        {"name": "Soft Doll", "desc": "Comfort object"},
        {"name": "First Shoes", "desc": "For early walkers"},
        {"name": "Baby Utensils", "desc": "For self-feeding"},
        {"name": "Playpen", "desc": "Safe containment"},
        {"name": "Musical Toys", "desc": "For auditory development"},
        {"name": "Shape Sorter", "desc": "Cognitive development"},
        {"name": "Baby Backpack", "desc": "For outings"},
        {"name": "Convertible High Chair", "desc": "Grows with child"},
        {"name": "Baby Sunglasses", "desc": "UV protection"},
        {"name": "Soft Ball", "desc": "For rolling and throwing"},
        {"name": "Baby Proofing Kit", "desc": "Safety for home"},
        {"name": "First Birthday Decor", "desc": "Planning ahead"},
        {"name": "Pull Toys", "desc": "For crawling babies"},
        {"name": "Touch-and-Feel Books", "desc": "Sensory books"},
        {"name": "Baby Pool Float", "desc": "Water safety"},
        {"name": "Growth Chart", "desc": "Track development"}
    ],
    "9-12 months": [
        {"name": "Size 3 Diapers", "desc": "For mobile babies"},
        {"name": "Push Walker", "desc": "For walking practice"},
        {"name": "Ride-On Toy", "desc": "For mobility play"},
        {"name": "Puzzle Blocks", "desc": "Early problem solving"},
        {"name": "Baby Tableware Set", "desc": "For independent eating"},
        {"name": "Stroller Fan", "desc": "For warm weather"},
        {"name": "Baby Back Carrier", "desc": "For hiking"},
        {"name": "First Words Books", "desc": "Language development"},
        {"name": "Baby Pool", "desc": "For water play"},
        {"name": "Sandbox Toys", "desc": "For outdoor play"},
        {"name": "Baby Balance Bike", "desc": "Early riding"},
        {"name": "Step Stool", "desc": "For reaching sink"},
        {"name": "Toddler Cups", "desc": "360-degree sippy cups"},
        {"name": "Baby Backpack Carrier", "desc": "For adventures"},
        {"name": "Play Kitchen", "desc": "Pretend play"},
        {"name": "Baby Tent", "desc": "For imaginative play"},
        {"name": "Water Table", "desc": "Outdoor sensory play"},
        {"name": "Toddler Bed", "desc": "Transition from crib"},
        {"name": "Baby Sign Language Kit", "desc": "Early communication"},
        {"name": "First Birthday Cake Smash Set", "desc": "Celebration"},
        {"name": "Baby Wagon", "desc": "For toys and rides"},
        {"name": "Toddler Silverware", "desc": "For self-feeding"},
        {"name": "Baby Rain Boots", "desc": "For puddle jumping"},
        {"name": "Magnetic Drawing Board", "desc": "Early art"},
        {"name": "Baby Photo Album", "desc": "First year memories"}
    ],
    "12-15 months": [
        {"name": "Size 4 Diapers", "desc": "For active toddlers"},
        {"name": "Toddler Shoes", "desc": "For first steps"},
        {"name": "Toddler Table and Chairs", "desc": "For play and meals"},
        {"name": "Building Blocks", "desc": "Large for easy handling"},
        {"name": "Picture Books", "desc": "For vocabulary building"},
        {"name": "Play Tool Set", "desc": "For imaginative play"},
        {"name": "Toddler Backpack", "desc": "For preschool prep"},
        {"name": "Balance Bike", "desc": "For coordination"},
        {"name": "Play Shopping Cart", "desc": "For pretend play"},
        {"name": "Bubble Machine", "desc": "Outdoor fun"},
        {"name": "Toddler Bed Rails", "desc": "For safe sleeping"},
        {"name": "Step Stool with Rails", "desc": "For bathroom independence"},
        {"name": "First Dollhouse", "desc": "For imaginative play"},
        {"name": "Toddler Umbrella", "desc": "For rainy days"},
        {"name": "Sandbox", "desc": "For outdoor play"},
        {"name": "Play Dough Set", "desc": "For sensory play"},
        {"name": "Toddler Helmet", "desc": "For bike safety"},
        {"name": "Potty Training Seat", "desc": "Early preparation"},
        {"name": "Toddler Step Stool", "desc": "For reaching sink"},
        {"name": "Chalkboard Easel", "desc": "For early art"},
        {"name": "Play Tunnel", "desc": "For physical activity"},
        {"name": "Toddler Gardening Set", "desc": "For outdoor learning"},
        {"name": "First Backpack", "desc": "For daycare"},
        {"name": "Toddler Raincoat", "desc": "For wet weather"},
        {"name": "Shape Puzzle", "desc": "For cognitive development"}
    ],
    "15-18 months": [
        {"name": "Size 5 Diapers", "desc": "For growing toddlers"},
        {"name": "Potty Chair", "desc": "For toilet training"},
        {"name": "Toddler Bed", "desc": "Transition from crib"},
        {"name": "Play Kitchen", "desc": "For imaginative play"},
        {"name": "Balance Bike", "desc": "For coordination"},
        {"name": "Toddler Tower", "desc": "For kitchen help"},
        {"name": "First Tricycle", "desc": "With parent push handle"},
        {"name": "Magnetic Letters", "desc": "For early literacy"},
        {"name": "Play Food Set", "desc": "For pretend cooking"},
        {"name": "Water Play Table", "desc": "Outdoor sensory"},
        {"name": "Toddler Backpack", "desc": "For daycare"},
        {"name": "First Puzzles", "desc": "With knobs for easy grip"},
        {"name": "Play Tent", "desc": "For imaginative space"},
        {"name": "Bubble Machine", "desc": "Outdoor fun"},
        {"name": "Toddler Chair", "desc": "For reading corner"},
        {"name": "First Art Supplies", "desc": "Washable crayons"},
        {"name": "Toy Doctor Kit", "desc": "For pretend play"},
        {"name": "Toddler Slide", "desc": "For backyard"},
        {"name": "Play Shopping Cart", "desc": "For imaginative play"},
        {"name": "First Train Set", "desc": "Simple wooden"},
        {"name": "Toddler Stool", "desc": "For bathroom independence"},
        {"name": "Sand and Water Table", "desc": "For sensory play"},
        {"name": "Play Tool Bench", "desc": "For pretend building"},
        {"name": "First Doll", "desc": "Soft body with clothes"},
        {"name": "Toddler Rain Boots", "desc": "For puddle jumping"}
    ],
    "18-21 months": [
        {"name": "Training Pants", "desc": "For potty learning"},
        {"name": "Toddler Bed", "desc": "If not already transitioned"},
        {"name": "Play Kitchen Accessories", "desc": "Expand play"},
        {"name": "First Scooter", "desc": "3-wheel for stability"},
        {"name": "Dress-Up Clothes", "desc": "For imaginative play"},
        {"name": "Play Cash Register", "desc": "For pretend shopping"},
        {"name": "Toddler Backpack", "desc": "For preschool prep"},
        {"name": "First Board Games", "desc": "Simple matching"},
        {"name": "Play Cleaning Set", "desc": "For imitating adults"},
        {"name": "Bubble Blower", "desc": "Outdoor fun"},
        {"name": "Toddler Camera", "desc": "For taking pictures"},
        {"name": "Play Garage", "desc": "For car play"},
        {"name": "First Musical Instruments", "desc": "Drum, xylophone"},
        {"name": "Toddler Gardening Tools", "desc": "For outdoor learning"},
        {"name": "Play Workbench", "desc": "For building play"},
        {"name": "First Backpack", "desc": "For daycare"},
        {"name": "Toddler Umbrella", "desc": "For rainy days"},
        {"name": "Play Dough Set", "desc": "With cutters"},
        {"name": "First Bike", "desc": "With training wheels"},
        {"name": "Toddler Chair", "desc": "For reading nook"},
        {"name": "Play Vet Set", "desc": "For animal care"},
        {"name": "Balance Board", "desc": "For physical development"},
        {"name": "First Magna-Tiles", "desc": "For building"},
        {"name": "Toddler Raincoat", "desc": "For wet weather"},
        {"name": "Play Tool Set", "desc": "For imitating adults"}
    ],
    "21-24 months": [
        {"name": "Potty Training Book", "desc": "For toilet learning"},
        {"name": "Toddler Bed", "desc": "If still in crib"},
        {"name": "Play Kitchen Food", "desc": "Expand pretend play"},
        {"name": "Balance Bike", "desc": "For coordination"},
        {"name": "First Backpack", "desc": "For preschool"},
        {"name": "Play Doctor Kit", "desc": "For imaginative play"},
        {"name": "Toddler Table Set", "desc": "For art and meals"},
        {"name": "First Puzzles", "desc": "More complex pieces"},
        {"name": "Play Cleaning Set", "desc": "For imitating adults"},
        {"name": "Bubble Machine", "desc": "Outdoor fun"},
        {"name": "Toddler Camera", "desc": "For taking pictures"},
        {"name": "Play Tool Bench", "desc": "For building play"},
        {"name": "First Musical Instruments", "desc": "Set of basics"},
        {"name": "Toddler Gardening Set", "desc": "For outdoor learning"},
        {"name": "Play Workbench", "desc": "For hammering"},
        {"name": "First Backpack", "desc": "For daycare"},
        {"name": "Toddler Umbrella", "desc": "For rainy days"},
        {"name": "Play Dough Set", "desc": "With accessories"},
        {"name": "First Bike", "desc": "With training wheels"},
        {"name": "Toddler Chair", "desc": "For reading corner"},
        {"name": "Play Vet Set", "desc": "For animal care"},
        {"name": "Balance Board", "desc": "For physical development"},
        {"name": "First Magna-Tiles", "desc": "For building"},
        {"name": "Toddler Raincoat", "desc": "For wet weather"},
        {"name": "Play Tool Set", "desc": "For imitating adults"}
    ]
}

# --- Enhanced Search Function ---
def search_products(query: str, num_results: int = 8) -> Tuple[List[Dict], Optional[Dict]]:
    """
    Returns: (list of products, debug_info)
    """
    if not API_KEY or not CSE_ID:
        st.error("❌ API not configured. Please check your secrets.toml")
        return [], None

    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": f"{query} buy online India",
        "searchType": "image",
        "num": min(num_results, 10),  # Free tier limit
        "safe": "active"
    }

    try:
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        response.raise_for_status()
        data = response.json()

        if "items" not in data:
            error_msg = data.get("error", {}).get("message", "No items found")
            return [], {"error": error_msg, "response": data}

        return data["items"], None

    except requests.exceptions.HTTPError as e:
        return [], {"error": str(e), "status_code": e.response.status_code}
    except Exception as e:
        return [], {"error": str(e)}

# --- Main App ---
def main():
    # Configure page
    

    # Initialize session state
    if "search_query" not in st.session_state:
        st.session_state.search_query = None
    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = False

    # --- Sidebar ---
    with st.sidebar:
        st.title("🤱 Motherly Heaven")
        st.markdown("### Shopping Preferences")

        # Step 1: Who are you shopping for?
        choice = st.radio(
            "Step 1: Who are you shopping for?",
            ["Mother", "Baby"],
            horizontal=True
        )

        # Step 2: Dynamic Questions
        if choice == "Mother":
            stage = st.selectbox("Current stage?", ["1st Trimester", "2nd Trimester", "3rd Trimester", "Postpartum"])
            first_time = st.radio("Is she a first-time mom?", ["Yes", "No"], horizontal=True)
            delivery = st.selectbox("Expected delivery method?", ["Vaginal", "C-section", "Not sure"])
            special = st.text_input("Any special needs (optional)?")
            st.session_state.user_answers = {
                "stage": stage,
                "first_time": first_time,
                "delivery": delivery,
                "special": special
            }

        elif choice == "Baby":
            age = st.selectbox("Age of baby?", ["0-3 months", "3-6 months", "6-9 months", "9-12 months", 
                                             "12-15 months", "15-18 months", "18-21 months", "21-24 months"])
            first_baby = st.radio("Is it their first baby?", ["Yes", "No"], horizontal=True)
            travel = st.radio("Planning any travel soon?", ["Yes", "No"], horizontal=True)
            st.session_state.user_answers = {
                "age": age,
                "first_baby": first_baby,
                "travel": travel
            }  
            # ... other baby-specific questions

        # Debug toggle
        st.session_state.debug_mode = st.checkbox("Debug Mode", False)

        if st.button("🔍 Find Products", type="primary"):
            st.session_state.search_query = None

    # --- Main Content ---
    if st.session_state.search_query is None:
        # Show recommendations
        st.title("Smart Product Recommender")
        
        products = MOTHER_PRODUCTS.get(stage, []) if choice == "Mother" else BABY_PRODUCTS.get(age, [])
        
        if products:
            st.subheader(f"🛍️ Recommended Products ")
            
            # Display products in 3 columns
            cols = st.columns(3)
            for idx, product in enumerate(products):
                with cols[idx % 3]:
                    if st.button(
                        f"🔍 {product['name']}",
                        key=f"prod_{idx}",
                        help=product["desc"]
                    ):
                        st.session_state.search_query = f"{product['name']} {product['desc']}"
                        st.rerun()
                    
                    st.caption(product["desc"])
        else:
            st.warning("No recommendations found. Please check your inputs.")

    else:
        # Show search results
        st.title(f"🔎 Search Results: {st.session_state.search_query.split(' buy')[0]}")
        
        results, debug_info = search_products(st.session_state.search_query)
        
        if not results:
            st.error("No products found. Try a different search term.")
            if debug_info:
                st.error(f"Error: {debug_info.get('error')}")
        else:
            # Display in 4-column grid
            cols = st.columns(4)
            for idx, item in enumerate(results):
                with cols[idx % 4]:
                    st.image(
                        item["link"],
                        # use_column_width=True,
                        caption=item["title"][:50] + ("..." if len(item["title"]) > 50 else "")
                    )
                    st.markdown(f"[🛒 View Product]({item['image']['contextLink']})")

        if st.button("← Back to Recommendations"):
            st.session_state.search_query = None
            st.rerun()

        # Debug info
        if st.session_state.debug_mode and debug_info:
            with st.expander("Debug Information"):
                st.json(debug_info)

if __name__ == "__main__":
    main()