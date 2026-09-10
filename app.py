import streamlit as st
from core.profile import FarmerProfile
from core.granite_engine import GraniteEngine
from core.prompts import build_agent_prompt
from services.weather_service import search_live_location, get_live_weather_by_coords
from services.market_service import get_mandi_rates
from services.rag_service import AgriRAGService
from services.sentinel_daemon import SentinelDaemon
from services.translation_service import translate_text, generate_audio, transcribe_audio_to_text
from services.vision_service import diagnose_leaf_image

st.set_page_config(page_title="AgriSense AI | National Crop Decision Platform", layout="wide", page_icon="🌾")

# Multi-Language UI Localization Dictionary
UI_TEXT = {
    "en": {
        "sidebar_header": "📋 Farmer Digital Profile",
        "sec_identity": "🌱 Crop & Field Identity",
        "sec_soil_water": "💧 Soil & Irrigation Parameters",
        "sec_location": "📍 Real-Time Location Search (Village / Taluk / State)",
        "crop": "Target Crop (Search or Select)",
        "soil": "Soil Classification (ICAR)",
        "age": "Crop Age (Days)",
        "loc_search_label": "Search Village / Town / Taluk:",
        "loc_search_placeholder": "Type here (e.g. Kokarenipalle, Sidlaghatta, Mandya...)",
        "loc_select_label": "Map Suggestions:",
        "irrigation": "Irrigation Method",
        "title": "🌾 AgriSense AI — Intelligent Agronomic Decision Engine",
        "active_profile": "Active Farm Profile",
        "sentinel_active": "🟢 24/7 Sentinel Active (Synchronous Multi-Zone Verification)",
        "temp": "🌡️ Temperature",
        "humidity": "💧 Humidity",
        "rain": "🌧️ Rain Probability",
        "price": "📈 Mandi Rate",
        "voice_query_label": "🎙️ Speak Farming Query / Symptoms (Speech-to-Text):",
        "text_query_label": "Or Enter Field Observations / Symptoms (Text):",
        "input_default": "Lower leaves turning yellow with slight brown spotting.",
        "leaf_upload": "📷 Upload Leaf / Fruit Photo (Optional)",
        "run_btn": "🚀 Run Farm Situation Analysis",
        "spinner": "Executing Grounded RAG Retrieval & Watsonx Granite-4-H-Small Fusion...",
        "tab1": "📊 Risk Assessment",
        "tab2": "💡 Grounded Advisory & Audio",
        "tab3": "📅 7-Day Action Plan",
        "tab4": "⚖️ Decision Simulation",
        "crop_health": "🌱 Crop Health",
        "weather_risk": "🌦️ Weather Risk",
        "pest_risk": "🐛 Pest Risk",
        "market_risk": "📈 Market Risk",
        "sources": "Verified ICAR/KVK Sources",
        "opt_a": "Option A",
        "opt_b": "Option B",
        "rec_choice": "🎯 Recommended Choice"
    },
    "kn": {
        "sidebar_header": "📋 ರೈತರ ಡಿಜಿಟಲ್ ಪ್ರೊಫೈಲ್",
        "sec_identity": "🌱 ಬೆಳೆ ಮತ್ತು ಜಮೀನಿನ ವಿವರ",
        "sec_soil_water": "💧 ಮಣ್ಣು ಮತ್ತು ನೀರಾವರಿ ನಿಯತಾಂಕಗಳು",
        "sec_location": "📍 ನೈಜ-ಸಮಯದ ಸ್ಥಳ ಹುಡುಕಾಟ (ಗ್ರಾಮ / ತಾಲೂಕು / ರಾಜ್ಯ)",
        "crop": "ಗುರಿ ಬೆಳೆ (ಹುಡುಕಿ ಅಥವಾ ಆಯ್ಕೆಮಾಡಿ)",
        "soil": "ಮಣ್ಣಿನ ವರ್ಗೀಕರಣ (ICAR)",
        "age": "ಬೆಳೆಯ ವಯಸ್ಸು (ದಿನಗಳು)",
        "loc_search_label": "ಗ್ರಾಮ / ಪಟ್ಟಣ / ತಾಲೂಕನ್ನು ಹುಡುಕಿ:",
        "loc_search_placeholder": "ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ (ಉದಾ: ಕೊಕ್ಕರೆನಿಪಲ್ಲೆ, ಶಿಡ್ಲಘಟ್ಟ, ಮಂಡ್ಯ...)",
        "loc_select_label": "ನಕ್ಷೆಯ ಸಲಹೆಗಳು:",
        "irrigation": "ನೀರಾವರಿ ವಿಧಾನ",
        "title": "🌾 ಅಗ್ರಿಸೆನ್ಸ್ AI — ಕೃಷಿ ನಿರ್ಧಾರ ಬೆಂಬಲ ವ್ಯವಸ್ಥೆ",
        "active_profile": "ಸಕ್ರಿಯ ಪ್ರೊಫೈಲ್",
        "sentinel_active": "🟢 24/7 ಸೆಂಟಿನೆಲ್ ಸಕ್ರಿಯವಾಗಿದೆ (ನೈಜ-ಸಮಯದ ಮೇಲ್ವಿಚಾರಣೆ)",
        "temp": "🌡️ ತಾಪಮಾನ",
        "humidity": "💧 ತೇವಾಂಶ",
        "rain": "🌧️ ಮಳೆಯ ಸಾಧ್ಯತೆ",
        "price": "📈 ಮಾರುಕಟ್ಟೆ ದರ",
        "voice_query_label": "🎙️ ಧ್ವನಿ ಮೂಲಕ ಪ್ರಶ್ನೆ ಕೇಳಿ (ಸ್ಪೀಚ್-ಟು-ಟೆಕ್ಸ್ಟ್):",
        "text_query_label": "ಅಥವಾ ವಿವರಗಳನ್ನು ಟೈಪ್ ಮಾಡಿ:",
        "input_default": "ಕೆಳಗಿನ ಎಲೆಗಳು ಸಣ್ಣ ಕಂದು ಕಲೆಗಳೊಂದಿಗೆ ಹಳದಿ ಬಣ್ಣಕ್ಕೆ ತಿರುಗುತ್ತಿವೆ.",
        "leaf_upload": "📷 ಎಲೆ ಅಥವಾ ಹಣ್ಣಿನ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ (ಐಚ್ಛಿಕ)",
        "run_btn": "🚀 ಕೃಷಿ ಪರಿಸ್ಥಿತಿ ವಿಶ್ಲೇಷಣೆ ಪ್ರಾರಂಭಿಸಿ",
        "spinner": "RAG ದತ್ತಾಂಶ ಮತ್ತು Watsonx Granite-4-H-Small ಮೂಲಕ ಅಧಿಕೃತ ವಿಶ್ಲೇಷಣೆ...",
        "tab1": "📊 ಅಪಾಯದ ಮೌಲ್ಯಮಾಪನ",
        "tab2": "💡 ಅಧಿಕೃತ ಸಲಹೆ ಮತ್ತು ಧ್ವನಿ",
        "tab3": "📅 7-ದಿನಗಳ ಕ್ರಿಯಾ ಯೋಜನೆ",
        "tab4": "⚖️ ನಿರ್ಧಾರ ಸಿಮ್ಯುಲೇಶನ್",
        "crop_health": "🌱 ಬೆಳೆ ಆರೋಗ್ಯ",
        "weather_risk": "🌦️ ಹವಾಮಾನ ಅಪಾಯ",
        "pest_risk": "🐛 ಕೀಟ ಅಪಾಯ",
        "market_risk": "📈 ಮಾರುಕಟ್ಟೆ ಅಪಾಯ",
        "sources": "ದೃಢೀಕೃತ ICAR/KVK ಆಧಾರಗಳು",
        "opt_a": "ಆಯ್ಕೆ A",
        "opt_b": "ಆಯ್ಕೆ B",
        "rec_choice": "🎯 ಶಿಫಾರಸು ಮಾಡಿದ ಆಯ್ಕೆ"
    },
    "hi": {
        "sidebar_header": "📋 किसान डिजिटल प्रोफाइल",
        "sec_identity": "🌱 फसल एवं खेत की जानकारी",
        "sec_soil_water": "💧 मिट्टी और सिंचाई प्रणाली",
        "sec_location": "📍 वास्तविक समय स्थान खोज (गाँव / तहसील / राज्य)",
        "crop": "लक्ष्य फसल (खोजें या चुनें)",
        "soil": "मिट्टी का वर्गीकरण (ICAR)",
        "age": "फसल की आयु (दिन)",
        "loc_search_label": "गाँव / कस्बा / तहसील खोजें:",
        "loc_search_placeholder": "यहाँ लिखें (उदा: कोकरेनिपल्ले, शिडलघट्टा, मांड्या...)",
        "loc_select_label": "मानचित्र सुझाव:",
        "irrigation": "सिंचाई का प्रकार",
        "title": "🌾 एग्रीसेंस AI — आधिकारिक निर्णय प्रणाली",
        "active_profile": "सक्रिय प्रोफाइल",
        "sentinel_active": "🟢 24/7 सेंटीनेल सक्रिय (वास्तविक समय निगरानी)",
        "temp": "🌡️ तापमान",
        "humidity": "💧 आर्द्रता",
        "rain": "🌧️ बारिश की संभावना",
        "price": "📈 मंडी भाव",
        "voice_query_label": "🎙️ बोलकर प्रश्न पूछें (स्पीच-टू-टेक्स्ट):",
        "text_query_label": "या फसल के लक्षण लिखें:",
        "input_default": "निचली पत्तियां हल्के भूरे धब्बों के साथ पीली पड़ रही हैं।",
        "leaf_upload": "📷 पत्ती या फल की फोटो अपलोड करें (वैकल्पिक)",
        "run_btn": "🚀 कृषि स्थिति विश्लेषण चलाएं",
        "spinner": "RAG डेटा और Watsonx Granite-4-H-Small के साथ प्रामाणिक विश्लेषण...",
        "tab1": "📊 जोखिम मूल्यांकन",
        "tab2": "💡 सटीक सलाह और ऑडियो",
        "tab3": "📅 7-दिवसीय कार्य योजना",
        "tab4": "⚖️ निर्णय सिमुलेशन",
        "crop_health": "🌱 फसल स्वास्थ्य",
        "weather_risk": "🌦️ मौसम जोखिम",
        "pest_risk": "🐛 कीट जोखिम",
        "market_risk": "📈 बाज़ार जोखिम",
        "sources": "सत्यापित ICAR/KVK स्रोत",
        "opt_a": "विकल्प A",
        "opt_b": "विकल्प B",
        "rec_choice": "🎯 अनुशंसित विकल्प"
    },
    "te": {
        "sidebar_header": "📋 రైతు డిజిటల్ ప్రొఫైల్",
        "sec_identity": "🌱 పంట మరియు పొలం వివరాలు",
        "sec_soil_water": "💧 నేల మరియు నీటిపారుదల",
        "sec_location": "📍 లైవ్ లొకేషన్ సెర్చ్ (గ్రామం / మండలం / రాష్ట్రం)",
        "crop": "లక్ష్య పంట (శోధించండి లేదా ఎంచుకోండి)",
        "soil": "నేల వర్గీకరణ (ICAR)",
        "age": "పంట వయస్సు (రోజులు)",
        "loc_search_label": "గ్రామం / పట్టణం / మండలం శోధించండి:",
        "loc_search_placeholder": "ఇక్కడ టైప్ చేయండి (ఉదా: కొక్కరాయనిపల్లె, చౌడూరు, ప్రొద్దుటూరు...)",
        "loc_select_label": "మ్యాప్ సూచనలు:",
        "irrigation": "నీటిపారుదల రకం",
        "title": "🌾 అగ్రిసెన్స్ AI — వ్యవసాయ నిర్ణయ మద్దతు వ్యవస్థ",
        "active_profile": "క్రియాశీల ప్రొఫైల్",
        "sentinel_active": "🟢 24/7 సెంటినెల్ యాక్టివ్ (నిరంతర నిఘా చక్రం)",
        "temp": "🌡️ ఉష్ణోగ్రత",
        "humidity": "💧 తేమ శాతం",
        "rain": "🌧️ వర్షపాత సంభావ్యత",
        "price": "📈 మార్కెట్ ధర",
        "voice_query_label": "🎙️ వాయిస్ ద్వారా ప్రశ్న అడగండి (స్పీచ్-టు-టెక్స్ట్):",
        "text_query_label": "లేదా పంట సమస్యల వివరాలు నమోదు చేయండి:",
        "input_default": "దిగువ ఆకులు చిన్న గోధుమ రంగు మచ్చలతో పసుపు రంగులోకి మారుతున్నాయి.",
        "leaf_upload": "📷 ఆకు లేదా పండు ఫోటో అప్‌లోడ్ చేయండి (ఐచ్ఛికం)",
        "run_btn": "🚀 పంట పరిస్థితి విశ్లేషణను ప్రారంభించండి",
        "spinner": "RAG డేటా మరియు Watsonx Granite-4-H-Small ద్వారా విశ్లేషణ...",
        "tab1": "📊 ప్రమాద అంచనా",
        "tab2": "💡 ప్రామాణిక సలహా & ఆడియో",
        "tab3": "📅 7-రోజుల కార్యాచరణ ప్రణాళిక",
        "tab4": "⚖️ నిర్ణయ సిమ్యులేషన్",
        "crop_health": "🌱 పంట ఆరోగ్యం",
        "weather_risk": "🌦️ వాతావరణ ముప్పు",
        "pest_risk": "🐛 పురుగుల ముప్పు",
        "market_risk": "📈 మార్కెట్ నష్టభయం",
        "sources": "ధృవీకరించబడిన ICAR/KVK ఆధారాలు",
        "opt_a": "ఎంపిక A",
        "opt_b": "ఎంపిక B",
        "rec_choice": "🎯 సిఫార్సు చేయబడిన ఎంపిక"
    }
}

# Complete Pan-India Crop, Soil, and Irrigation Taxonomy
DROPDOWN_DATA = {
    "crops": {
        "keys": [
            "Rice (Paddy)", "Wheat", "Maize (Corn)", "Jowar (Sorghum)", "Bajra (Pearl Millet)",
            "Ragi (Finger Millet)", "Foxtail Millet (Navane/Kangni/Korra)", "Little Millet (Samai)",
            "Kodo Millet (Harka/Kodra/Arikelu)", "Barnyard Millet (Oodalu/Sanwa/Udalu)", 
            "Proso Millet (Barri/Variga)", "Barley (Jau)", "Oats",
            "Chickpea (Bengal Gram / Chana)", "Pigeon Pea (Tur / Arhar / Togari / Kandi)", 
            "Green Gram (Moong / Hesaru / Pesalu)", "Black Gram (Urad / Uddina / Minumulu)", 
            "Lentil (Masoor)", "Horse Gram (Kulthi / Huruli / Ulavalu)", 
            "Cowpea (Lobia / Alasande / Alasandalu)", "Field Pea (Matar)", 
            "Moth Bean (Matki)", "Rajma (Kidney Bean)", "Soybean",
            "Groundnut (Peanut)", "Mustard & Rapeseed (Sarson / Sasive)", "Sunflower", 
            "Sesame (Til / Ellu / Nuvvulu)", "Castor Seed (Haralu / Aamudalu)", 
            "Safflower (Kardi / Kusuma)", "Linseed (Flaxseed / Alsi)", "Niger Seed (Gurellu / Uchellu)",
            "Cotton (Kapas / Hatti / Patti)", "Sugarcane (Khabbu / Cheruku)", "Jute (Pat)", 
            "Tobacco", "Tea", "Coffee", "Rubber", "Coconut (Thengu / Kobbari)", 
            "Arecanut (Betel Nut / Adike / Vakka)", "Cashew Nut (Geru / Jeedipappu)", 
            "Betel Leaf (Paan / Velyada Ele / Tamalapaaku)", "Mulberry (Sericulture)",
            "Tomato", "Potato (Aloo)", "Onion (Pyaaz / Eerulli / Ullipaaya)", "Chilli (Green / Raw)", 
            "Brinjal (Eggplant / Baingan / Badane)", "Okra (Ladies Finger / Bhindi / Bhendi)", 
            "Cabbage", "Cauliflower", "Garlic (Lahsun / Bellulli / Vellulli)", 
            "Bottle Gourd (Lauki / Sorekayi / Sorakaya)", "Bitter Gourd (Karela / Hagalakayi / Kakarakaya)", 
            "Ridge Gourd (Torai / Heerekayi / Beerakaya)", "Snake Gourd (Padwal / Padavalakayi / Potlakaya)", 
            "Ash Gourd (Petha / Boodu Kumbalakayi / Boodida Gummadikaya)", 
            "Pumpkin (Kaddu / Kumbalakayi / Gummadikaya)", "Cucumber (Kheera / Southekayi / Dosakaya)", 
            "Radish (Mooli / Moolangi / Mullangi)", "Carrot (Gajar)", "Beetroot", 
            "Drumstick (Moringa / Nuggekayi / Munagakaya)", "Spinach (Palak / Palak Soppu / Paalakoora)", 
            "Fenugreek Leaves (Methi / Menthya Soppu / Menthikoora)", "Coriander Leaves (Kothambari)",
            "Tapioca (Cassava / Maravalli)", "Sweet Potato (Shakarkand / Sihi Genasu / Chilagada Dumpa)", 
            "Elephant Foot Yam (Suran / Suvarna Gedde / Kanda Gadda)", "Colocasia (Arbi / Kesuvina Gedde / Chaama Dumpa)",
            "Dry Red Chilli", "Turmeric (Haldi / Arishina / Pasupu)", "Ginger (Adrak / Shunti / Allam)", 
            "Black Pepper (Kali Mirch / Menasu / Miriyalu)", "Cardamom (Elaichi / Yelakki / Yelakulu)", 
            "Cumin (Jeera / Jeerige / Jeelakarra)", "Coriander Seeds (Dhania)", 
            "Fennel (Saunf / Sompu)", "Fenugreek Seeds (Methi Dana)", "Ajwain (Carom Seeds / Oma / Vaamu)",
            "Mango (Aam / Mavu / Mamidi)", "Banana (Kela / Baale / Arati)", "Pomegranate (Anar / Dalimbe / Danimma)", 
            "Guava (Amrood / Seebe / Jama)", "Papaya (Papita / Parangi / Boppayi)", 
            "Citrus (Sweet Lime / Mosambi / Battayi)", "Lemon (Acid Lime / Nimbu / Nimbe / Nimma)", 
            "Grapes (Angoor / Drakshi / Draksha)", "Watermelon (Tarbooj / Kallangadi / Pucha Kaya)", 
            "Muskmelon (Kharbooja)", "Custard Apple (Seethaphal)", "Sapota (Chiku)", 
            "Jackfruit (Halasu / Panasa Kaya)", "Pineapple (Ananas)", "Apple", "Dragon Fruit",
            "Jasmine (Mallige / Malle)", "Marigold (Genda / Chendu Hoovu / Banthi)", 
            "Rose (Gulab / Gulabi)", "Chrysanthemum (Sevanthige / Chamanthi)", 
            "Ashwagandha", "Lemongrass", "Mint (Pudina)"
        ],
        "en": [
            "Rice (Paddy)", "Wheat", "Maize (Corn)", "Jowar (Sorghum)", "Bajra (Pearl Millet)",
            "Ragi (Finger Millet)", "Foxtail Millet (Navane)", "Little Millet (Samai)",
            "Kodo Millet (Harka)", "Barnyard Millet (Oodalu)", "Proso Millet (Barri)", "Barley (Jau)", "Oats",
            "Chickpea (Bengal Gram)", "Pigeon Pea (Tur / Arhar)", "Green Gram (Moong)", "Black Gram (Urad)",
            "Lentil (Masoor)", "Horse Gram (Kulthi)", "Cowpea (Lobia)", "Field Pea (Matar)",
            "Moth Bean", "Rajma (Kidney Bean)", "Soybean",
            "Groundnut (Peanut)", "Mustard & Rapeseed", "Sunflower", "Sesame (Til)", "Castor Seed",
            "Safflower (Kusuma)", "Linseed (Flaxseed)", "Niger Seed",
            "Cotton (Kapas)", "Sugarcane", "Jute", "Tobacco", "Tea", "Coffee", "Rubber", "Coconut",
            "Arecanut (Betel Nut)", "Cashew Nut", "Betel Leaf (Paan)", "Mulberry",
            "Tomato", "Potato", "Onion", "Chilli (Green)", "Brinjal (Eggplant)", "Okra (Ladies Finger)",
            "Cabbage", "Cauliflower", "Garlic", "Bottle Gourd (Lauki)", "Bitter Gourd (Karela)",
            "Ridge Gourd (Torai)", "Snake Gourd", "Ash Gourd", "Pumpkin", "Cucumber", "Radish",
            "Carrot", "Beetroot", "Drumstick (Moringa)", "Spinach (Palak)", "Fenugreek Leaves (Methi)", "Coriander Leaves",
            "Tapioca (Cassava)", "Sweet Potato", "Elephant Foot Yam (Suran)", "Colocasia (Arbi)",
            "Dry Red Chilli", "Turmeric", "Ginger", "Black Pepper", "Cardamom", "Cumin (Jeera)",
            "Coriander Seeds (Dhania)", "Fennel (Saunf)", "Fenugreek Seeds", "Ajwain",
            "Mango", "Banana", "Pomegranate", "Guava", "Papaya", "Citrus (Mosambi)", "Lemon",
            "Grapes", "Watermelon", "Muskmelon", "Custard Apple", "Sapota (Chiku)", "Jackfruit", "Pineapple", "Apple", "Dragon Fruit",
            "Jasmine", "Marigold", "Rose", "Chrysanthemum", "Ashwagandha", "Lemongrass", "Mint (Pudina)"
        ],
        "kn": [
            "ಭತ್ತ (Rice/Paddy)", "ಗೋಧಿ (Wheat)", "ಮೆಕ್ಕೆಜೋಳ (Maize)", "ಜೋಳ (Jowar)", "ಸಜ್ಜೆ (Bajra)",
            "ರಾಗಿ (Ragi)", "ನವಣೆ (Foxtail Millet)", "ಸಾಮೆ (Little Millet)",
            "ಹಾರಕ (Kodo Millet)", "ಊದಲು (Barnyard Millet)", "ಬರಗು (Proso Millet)", "ಜವೆಗೋಧಿ (Barley)", "ಓಟ್ಸ್ (Oats)",
            "ಕಡಲೆ (Chickpea/Chana)", "ತೊಗರಿ (Tur/Pigeon Pea)", "ಹೆಸರುಕಾಳು (Moong)", "ಉದ್ದಿನಕಾಳು (Urad)",
            "ಮಸೂರ (Lentil)", "ಹುರುಳಿ (Horse Gram)", "ಅಲಸಂದೆ (Cowpea)", "ಬಟಾಣಿ (Pea)",
            "ಮಡಿಕೆ ಕಾಳು (Moth Bean)", "ರಾಜ್ಮಾ (Rajma)", "ಸೋಯಾಬೀನ್ (Soybean)",
            "ಕಡಲೆಕಾಯಿ (Groundnut)", "ಸಾಸಿವೆ (Mustard)", "ಸೂರ್ಯಕಾಂತಿ (Sunflower)", "ಎಳ್ಳು (Sesame)", "ಹರಳು (Castor)",
            "ಕುಸುಮೆ (Safflower)", "ಅಗಸೆ ಬೀಜ (Linseed)", "ಗುರೆಳ್ಳು / ಹುಚ್ಚೆಳ್ಳು (Niger Seed)",
            "ಹತ್ತಿ (Cotton)", "ಕಬ್ಬು (Sugarcane)", "ಸೆಣಬು (Jute)", "ತಂಬಾಕು (Tobacco)", "ಚಹಾ (Tea)", "ಕಾಫಿ (Coffee)", "ರಬ್ಬರ್ (Rubber)", "ತೆಂಗು (Coconut)",
            "ಅಡಿಕೆ (Arecanut)", "ಗೋಡಂಬಿ (Cashew)", "ವೀಳ್ಯದೆಲೆ (Betel Leaf)", "ಹಿಪ್ಪುನೇರಳೆ (Mulberry)",
            "ಟೊಮೇಟೊ (Tomato)", "ಆಲೂಗಡ್ಡೆ (Potato)", "ಈರುಳ್ಳಿ (Onion)", "ಹಸಿಮೆಣಸಿನಕಾಯಿ (Green Chilli)", "ಬದನೆಕಾಯಿ (Brinjal)", "ಬೆಂಡೆಕಾಯಿ (Okra)",
            "ಎಲೆಕೋಸು (Cabbage)", "ಹೂಕೋಸು (Cauliflower)", "ಬೆಳ್ಳುಳ್ಳಿ (Garlic)", "ಸೋರೆಕಾಯಿ (Bottle Gourd)", "ಹಾಗಲಕಾಯಿ (Bitter Gourd)",
            "ಹೀರೆಕಾಯಿ (Ridge Gourd)", "ಪಡವಲಕಾಯಿ (Snake Gourd)", "ಬೂದು ಕುಂಬಳಕಾಯಿ (Ash Gourd)", "ಕುಂಬಳಕಾಯಿ (Pumpkin)", "ಸೌತೆಕಾಯಿ (Cucumber)", "ಮೂಲಂಗಿ (Radish)",
            "ಕ್ಯಾರೆಟ್ (Carrot)", "ಬೀಟ್‌ರೂಟ್ (Beetroot)", "ನುಗ್ಗೆಕಾಯಿ (Drumstick)", "ಪಾಲಕ್ ಸೊಪ್ಪು (Spinach)", "ಮೆಂತ್ಯ ಸೊಪ್ಪು (Fenugreek)", "ಕೊತ್ತಂಬರಿ ಸೊಪ್ಪು (Coriander)",
            "ಮರಗೆಣಸು (Tapioca)", "ಸಿಹಿ ಗೆಣಸು (Sweet Potato)", "ಸುವರ್ಣ ಗಡ್ಡೆ (Yam)", "ಕೆಸುವಿನ ಗಡ್ಡೆ (Colocasia)",
            "ಒಣ ಮೆಣಸಿನಕಾಯಿ (Dry Chilli)", "ಅರಿಶಿನ (Turmeric)", "ಶುಂಠಿ (Ginger)", "ಕಾಳುಮೆಣಸು (Black Pepper)", "ಏಲಕ್ಕಿ (Cardamom)", "ಜೀರಿಗೆ (Cumin)",
            "ಧನಿಯಾ / ಕೊತ್ತಂಬರಿ ಬೀಜ (Coriander Seeds)", "ಸೋಂಪು (Fennel)", "ಮೆಂತ್ಯ ಕಾಳು (Methi Seeds)", "ಓಮ (Ajwain)",
            "ಮಾವಿನಹಣ್ಣು (Mango)", "ಬಾಳೆಹಣ್ಣು (Banana)", "ದಾಳಿಂಬೆ (Pomegranate)", "ಸೀಬೆಹಣ್ಣು (Guava)", "ಪರಂಗಿ / ಪಪ್ಪಾಯಿ (Papaya)", "ಮೋಸಂಬಿ (Sweet Lime)", "ನಿಂಬೆಹಣ್ಣು (Lemon)",
            "ದ್ರಾಕ್ಷಿ (Grapes)", "ಕಲ್ಲಂಗಡಿ (Watermelon)", "ಖರ್ಬೂಜ (Muskmelon)", "ಸೀತಾಫಲ (Custard Apple)", "ಚಿಕ್ಕು / ಸಪೋಟ (Sapota)", "ಹಲಸಿನಹಣ್ಣು (Jackfruit)", "ಅನಾನಸ್ (Pineapple)", "ಸೇಬು (Apple)", "ಡ್ರ್ಯಾಗನ್ ಫ್ರೂಟ್ (Dragon Fruit)",
            "ಮಲ್ಲಿಗೆ (Jasmine)", "ಚೆಂಡು ಹೂವು (Marigold)", "ಗುಲಾಬಿ (Rose)", "ಸೇವಂತಿಗೆ (Chrysanthemum)", "ಅಶ್ವಗಂಧ (Ashwagandha)", "ಲೆಮನ್‌ಗ್ರಾಸ್ (Lemongrass)", "ಪುದೀನ (Mint)"
        ],
        "hi": [
            "धान / चावल (Rice/Paddy)", "गेहूं (Wheat)", "मक्का (Maize)", "ज्वार (Jowar)", "बाजरा (Bajra)",
            "रागी / मडुआ (Ragi)", "कंगनी (Foxtail Millet)", "कुटकी / समाई (Little Millet)",
            "कोदो (Kodo Millet)", "सांवां (Barnyard Millet)", "चीना / बरी (Proso Millet)", "जौ (Barley)", "जई (Oats)",
            "चना (Chickpea/Chana)", "अरहर / तुअर (Tur/Pigeon Pea)", "मूंग (Green Gram)", "उड़द (Black Gram)",
            "मसूर (Lentil)", "कुलथी (Horse Gram)", "लोबिया / चौलाई (Cowpea)", "मटर (Field Pea)",
            "मोठ (Moth Bean)", "राजमा (Kidney Bean)", "सोयाबीन (Soybean)",
            "मूंगफली (Groundnut)", "सरसों / राई (Mustard)", "सूरजमुखी (Sunflower)", "तिल (Sesame)", "अरंडी (Castor)",
            "कुसुम (Safflower)", "अलसी (Linseed)", "रामतिल (Niger Seed)",
            "कपास / रुई (Cotton)", "गन्ना (Sugarcane)", "पटसन / जूट (Jute)", "तंबाकू (Tobacco)", "चाय (Tea)", "कॉफी (Coffee)", "रबर (Rubber)", "नारियल (Coconut)",
            "सुपारी (Arecanut)", "काजू (Cashew)", "पान का पत्ता (Betel Leaf)", "शहतूत (Mulberry)",
            "टमाटर (Tomato)", "आलू (Potato)", "प्याज (Onion)", "हरी मिर्च (Green Chilli)", "बैंगन (Brinjal)", "भिंडी (Okra)",
            "पत्तागोभी (Cabbage)", "फूलगोभी (Cauliflower)", "लहसुन (Garlic)", "लौकी (Bottle Gourd)", "करेला (Bitter Gourd)",
            "तोरई (Ridge Gourd)", "चिचिंडा (Snake Gourd)", "पेठा / सफेद कद्दू (Ash Gourd)", "कद्दू (Pumpkin)", "खीरा (Cucumber)", "मूली (Radish)",
            "गाजर (Carrot)", "चुकंदर (Beetroot)", "सहजन / मुनगा (Drumstick)", "पालक (Spinach)", "मेथी पत्ता (Fenugreek)", "धनिया पत्ता (Coriander)",
            "कसावा / टैपिओका (Tapioca)", "शकरकंद (Sweet Potato)", "जिमीकंद / सूरन (Yam)", "अरबी (Colocasia)",
            "सूखी लाल मिर्च (Dry Chilli)", "हल्दी (Turmeric)", "अदरक (Ginger)", "काली मिर्च (Black Pepper)", "इलायची (Cardamom)", "जीरा (Cumin)",
            "धनिया बीज (Coriander Seeds)", "सौंफ (Fennel)", "मेथी दाना (Methi Seeds)", "अजवाइन (Ajwain)",
            "आम (Mango)", "केला (Banana)", "अनार (Pomegranate)", "अमरूद (Guava)", "पपीता (Papaya)", "मौसमी (Sweet Lime)", "नींबू (Lemon)",
            "अंगूर (Grapes)", "तरबूज (Watermelon)", "खरबूजा (Muskmelon)", "शरीफा / सीताफल (Custard Apple)", "चीकू (Sapota)", "कटहल (Jackfruit)", "अनानास (Pineapple)", "सेब (Apple)", "ड्रैगन फ्रूट (Dragon Fruit)",
            "चमेली / मोगरा (Jasmine)", "गेंदा (Marigold)", "गुलाब (Rose)", "गुलदाउदी (Chrysanthemum)", "अश्वगंधा (Ashwagandha)", "लेमनग्रास (Lemongrass)", "पुदीना (Mint)"
        ],
        "te": [
            "వరి / ధాన్యం (Rice/Paddy)", "గోధుమ (Wheat)", "మొక్కజొన్న (Maize)", "జొన్నలు (Jowar)", "సజ్జలు (Bajra)",
            "రాగులు / తైదలు (Ragi)", "కొర్రలు (Foxtail Millet)", "సామలు (Little Millet)",
            "అరికెలు (Kodo Millet)", "ఊదలు (Barnyard Millet)", "వరిగెలు (Proso Millet)", "బార్లీ (Barley)", "ఓట్స్ (Oats)",
            "శనగలు (Chickpea/Chana)", "కందులు (Tur/Kandi)", "పెసలు (Moong)", "మినుములు (Urad)",
            "మసూర పప్పు (Lentil)", "ఉలవలు (Horse Gram)", "అలసందలు / బొబ్బర్లు (Cowpea)", "బఠానీ (Pea)",
            "మొలక బీన్స్ (Moth Bean)", "రాజ్మా (Rajma)", "సోయాబీన్ (Soybean)",
            "వేరుశనగ (Groundnut)", "ఆవాలు (Mustard)", "పొద్దుతిరుగుడు (Sunflower)", "నువ్వులు (Sesame)", "ఆముదం (Castor)",
            "కుసుమ (Safflower)", "అవిసె గింజలు (Linseed)", "గుర్రాలు / వెర్రినువ్వులు (Niger Seed)",
            "పత్తి (Cotton)", "చెరకు (Sugarcane)", "జనపనార (Jute)", "పొగాకు (Tobacco)", "టీ (Tea)", "కాఫీ (Coffee)", "రబ్బరు (Rubber)", "కొబ్బరి (Coconut)",
            "పోకచెక్క / వక్క (Arecanut)", "జీడిపప్పు (Cashew)", "తమలపాకు (Betel Leaf)", "మల్బరీ (Mulberry)",
            "టమోటా (Tomato)", "బంగాళాదుంప (Potato)", "ఉల్లిపాయ (Onion)", "పచ్చిమిర్చి (Green Chilli)", "వంకాయ (Brinjal)", "బెండకాయ (Okra)",
            "క్యాబేజీ (Cabbage)", "కాలీఫ్లవర్ (Cauliflower)", "వెల్లుల్లి (Garlic)", "సొరకాయ (Bottle Gourd)", "కాకరకాయ (Bitter Gourd)",
            "బీరకాయ (Ridge Gourd)", "పొట్లకాయ (Snake Gourd)", "బూడిద గుమ్మడికాయ (Ash Gourd)", "గుమ్మడికాయ (Pumpkin)", "దోసకాయ (Cucumber)", "ముల్లంగి (Radish)",
            "క్యారెట్ (Carrot)", "బీట్‌రూట్ (Beetroot)", "మునగకాయ (Drumstick)", "పాలకూర (Spinach)", "మెంతికూర (Fenugreek)", "కొత్తిమీర (Coriander)",
            "కర్ర పెండలం (Tapioca)", "చిలగడదుంప (Sweet Potato)", "కంద గడ్డ (Yam)", "చామదుంప (Colocasia)",
            "ఎండిన మిరపకాయ (Dry Chilli)", "పసుపు (Turmeric)", "అల్లం (Ginger)", "మిరియాలు (Black Pepper)", "యాలకులు (Cardamom)", "జీలకర్ర (Cumin)",
            "ధనియాలు (Coriander Seeds)", "సోంపు (Fennel)", "మెంతులు (Methi Seeds)", "వాము (Ajwain)",
            "మామిడి (Mango)", "అరటి (Banana)", "దానిమ్మ (Pomegranate)", "జామ (Guava)", "బొప్పాయి (Papaya)", "బత్తాయి (Sweet Lime)", "నిమ్మకాయ (Lemon)",
            "ద్రాక్ష (Grapes)", "పుచ్చకాయ (Watermelon)", "ఖర్బూజ (Muskmelon)", "సీతాఫలం (Custard Apple)", "సపోటా (Sapota)", "పనసకాయ (Jackfruit)", "అనాస (Pineapple)", "యాపిల్ (Apple)", "డ్రాగన్ ఫ్రూట్ (Dragon Fruit)",
            "మల్లెపూలు (Jasmine)", "బంతిపూలు (Marigold)", "గులాబీ (Rose)", "చామంతి (Chrysanthemum)", "అశ్వగంధ (Ashwagandha)", "నిమ్మగడ్డి (Lemongrass)", "పుదీనా (Mint)"
        ]
    },
    "soils": {
        "keys": ["Alluvial Soil", "Black Cotton Soil", "Red and Yellow Soil", "Laterite Soil", "Arid Desert Soil", "Saline Alkaline Soil", "Peaty Soil", "Mountain Soil"],
        "en": ["Alluvial Soil", "Black Cotton Soil (Regur)", "Red and Yellow Soil", "Laterite Soil", "Arid / Desert Soil", "Saline and Alkaline Soil", "Peaty and Marshy Soil", "Mountain Soil"],
        "kn": ["ಮೆಕ್ಕಲು ಮಣ್ಣು (Alluvial)", "ಕಪ್ಪು ಹತ್ತಿ ಮಣ್ಣು (Black Cotton)", "ಕೆಂಪು ಮತ್ತು ಹಳದಿ ಮಣ್ಣು (Red & Yellow)", "ಲ್ಯಾಟರೈಟ್ ಮಣ್ಣು (Laterite)", "ಮರುಭೂಮಿ ಮಣ್ಣು (Arid)", "ಕ್ಷಾರೀಯ ಮಣ್ಣು (Saline)", "ಜವುಗು ಮಣ್ಣು (Peaty)", "ಪರ್ವತ ಮಣ್ಣು (Mountain)"],
        "hi": ["जलोढ़ मिट्टी (Alluvial)", "काली मिट्टी (Black Cotton)", "लाल और पीली मिट्टी (Red & Yellow)", "लेटराइट मिट्टी (Laterite)", "शुष्क/रेगिस्तानी मिट्टी (Arid)", "लवणीय/क्षारीय मिट्टी (Saline)", "पीट/दलदली मिट्टी (Peaty)", "पर्वतीय मिट्टी (Mountain)"],
        "te": ["ఒండ్రు నేల (Alluvial)", "నల్ల రేగడి నేల (Black Cotton)", "ఎర్ర మరియు పసుపు నేల (Red & Yellow)", "లేటరైట్ నేల (Laterite)", "ఎడారి నేల (Arid)", "చౌడు నేల (Saline)", "పీట్/చిత్తడి నేల (Peaty)", "పర్వత నేల (Mountain)"]
    },
    "irrigations": {
        "keys": ["Drip", "Sprinkler", "Furrow / Flood", "Rainfed", "Check Basin"],
        "en": ["Drip Irrigation", "Sprinkler Irrigation", "Furrow / Flood Irrigation", "Rainfed (Dryland)", "Check Basin"],
        "kn": ["ಹನಿ ನೀರಾವರಿ (Drip)", "ತುಂತುರು ನೀರಾವರಿ (Sprinkler)", "ಕಾಲುವೆ/ಪ್ರವಾಹ ನೀರಾವರಿ (Flood)", "ಮಳೆ ಆಶ್ರಿತ (Rainfed)", "ಮಡಿ ನೀರಾವರಿ (Basin)"],
        "hi": ["ड्रिप / टपक सिंचाई (Drip)", "स्प्रिंकलर / छिड़काव (Sprinkler)", "नाली / बाढ़ सिंचाई (Flood)", "वर्षा आधारित (Rainfed)", "थाला / द्रोणी सिंचाई (Basin)"],
        "te": ["బిందు సేద్యం (Drip)", "తుంపర సేద్యం (Sprinkler)", "కాలువ / వరద పారుదల (Flood)", "వర్షాధారం (Rainfed)", "మడి నీటిపారుదల (Basin)"]
    }
}

# Singletons & Session Initialization
if "engine" not in st.session_state:
    st.session_state.engine = GraniteEngine()
if "rag" not in st.session_state:
    st.session_state.rag = AgriRAGService()
if "sentinel" not in st.session_state:
    st.session_state.sentinel = SentinelDaemon()
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Sidebar Language Selection
lang_choice = st.sidebar.radio("🌐 Language / ಭಾಷೆ / भाषा / భాష", ["English", "ಕನ್ನಡ (Kannada)", "हिंदी (Hindi)", "తెలుగు (Telugu)"])
lang_map = {"English": "en", "ಕನ್ನಡ (Kannada)": "kn", "हिंदी (Hindi)": "hi", "తెలుగు (Telugu)": "te"}
lang = lang_map.get(lang_choice, "en")
T = UI_TEXT.get(lang, UI_TEXT["en"])

st.sidebar.title(T["sidebar_header"])

# SECTION 1: Crop & Field Identity
st.sidebar.markdown(f"### {T['sec_identity']}")
crop_labels = DROPDOWN_DATA["crops"][lang]
crop_choice = st.sidebar.selectbox(T["crop"], crop_labels, key="sel_crop")
crop = DROPDOWN_DATA["crops"]["keys"][crop_labels.index(crop_choice)]

age = st.sidebar.slider(T["age"], 5, 150, 35, key="slider_age")

st.sidebar.divider()

# SECTION 2: Soil & Irrigation Parameters
st.sidebar.markdown(f"### {T['sec_soil_water']}")
soil_labels = DROPDOWN_DATA["soils"][lang]
soil_choice = st.sidebar.selectbox(T["soil"], soil_labels, key="sel_soil")
soil = DROPDOWN_DATA["soils"]["keys"][soil_labels.index(soil_choice)]

irr_labels = DROPDOWN_DATA["irrigations"][lang]
irr_choice = st.sidebar.selectbox(T["irrigation"], irr_labels, key="sel_irr")
irrigation = DROPDOWN_DATA["irrigations"]["keys"][irr_labels.index(irr_choice)]

st.sidebar.divider()

# SECTION 3: Dynamic Real-Time Location Search with Map Suggestions
st.sidebar.markdown(f"### {T['sec_location']}")
search_query = st.sidebar.text_input(
    T["loc_search_label"], 
    value="Chikkaballapur", 
    placeholder=T["loc_search_placeholder"]
)

matched_locations = search_live_location(search_query) if search_query else []

if matched_locations:
    loc_options = [loc["short_label"] for loc in matched_locations]
    selected_loc_choice = st.sidebar.selectbox(T["loc_select_label"], loc_options, key="live_map_suggest_box")
    selected_loc = matched_locations[loc_options.index(selected_loc_choice)]
    
    current_lat = selected_loc["lat"]
    current_lon = selected_loc["lon"]
    current_district = selected_loc["district"]
    effective_display_location = selected_loc["short_label"]
else:
    current_lat, current_lon = 13.4355, 77.7275
    current_district = "Chikkaballapur"
    effective_display_location = f"{search_query} (Regional Coordinates)"

profile = FarmerProfile(
    crop=crop, soil_type=soil, crop_age_days=age, 
    district=effective_display_location, irrigation_type=irrigation, language=lang
)

# Main Dashboard Header
st.title(T["title"])
st.caption(f"{T['active_profile']}: **{profile.summary()}**")
st.success(T["sentinel_active"])

# Multi-Tier Risk Evaluation (Red Alert vs Moderate Watch vs Safe)
weather = get_live_weather_by_coords(current_lat, current_lon)
alert = st.session_state.sentinel.evaluate_risk(
    profile, 
    weather, 
    rag_service=st.session_state.rag, 
    engine=st.session_state.engine
)

if alert:
    risk_tier = alert.get("risk_level", "HIGH")
    alert_title = translate_text(alert.get('title', ''), lang)
    alert_msg = translate_text(alert.get('message', ''), lang)
    
    with st.container():
        if risk_tier == "HIGH":
            st.error(f"🚨 **[RED ALERT - HIGH RISK] {alert_title}**")
        else:
            st.warning(f"⚠️ **[MODERATE RISK - WATCH] {alert_title}**")
            
        st.write(alert_msg)
        for step in alert.get('protection_steps', []):
            st.markdown(f"• {translate_text(step, lang)}")
        
        alert_audio = generate_audio(f"{alert_title}. {alert_msg}", lang)
        if alert_audio:
            st.audio(alert_audio, format="audio/mp3")

st.divider()

# Live Real-Time Telemetry & APMC Market Intelligence
market = get_mandi_rates(crop, current_district)

t1, t2, t3, t4 = st.columns(4)
t1.metric(T["temp"], f"{weather['temperature']} °C", help=f"Coordinates: {weather['lat']}, {weather['lon']} | {weather['status']}")
t2.metric(T["humidity"], f"{weather['humidity']} %", help=f"Status: {weather['status']}")
t3.metric(T["rain"], f"{weather['rain_prob']} %", help=f"Status: {weather['status']}")
t4.metric(
    label=f"{T['price']} ({crop_choice.split(' ')[0]})",
    value=f"₹ {market['modal_price']} / Qtl",
    delta=market.get("delta_formatted", "0.0%"),
    delta_color="normal",
    help=f"Market: {market['market']} | Trend: {market.get('trend_label', 'Stable')} | National Benchmark: ₹{market.get('national_avg', market['modal_price'])}/Qtl"
)

st.divider()

# Multimodal User Diagnostic Inputs
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    voice_query_file = st.audio_input(T["voice_query_label"], key="main_voice_in")
    voice_transcribed = transcribe_audio_to_text(voice_query_file, lang) if voice_query_file else ""
    
    current_text_value = voice_transcribed if voice_transcribed else T["input_default"]
    query = st.text_input(T["text_query_label"], value=current_text_value)

with col_in2:
    uploaded_leaf = st.file_uploader(T["leaf_upload"], type=["jpg", "png", "jpeg"])

if st.button(T["run_btn"], type="primary"):
    with st.spinner(T["spinner"]):
        vision_result = diagnose_leaf_image(uploaded_leaf) if uploaded_leaf else None
        
        # When an image is provided, integrate its visual diagnosis directly into the agronomic query
        if vision_result:
            st.info(
                f"📷 **Visual Diagnosis**: {vision_result['detected_condition']} "
                f"({vision_result['confidence']} confidence)\n\n"
                f"*Observed Pathology*: {vision_result['visual_markers']}"
            )
            enhanced_query = (
                f"Visual examination confirmed {vision_result['detected_condition']} on {vision_result['affected_organ']}. "
                f"Observed pathology: {vision_result['visual_markers']}."
            )
            if query and query != T["input_default"]:
                enhanced_query += f" Additional field notes: {query}"
        else:
            enhanced_query = query

        docs = st.session_state.rag.retrieve_guidance(crop, enhanced_query)
        sys_p, usr_p = build_agent_prompt(profile, weather, market, docs, enhanced_query)
        st.session_state.analysis_result = st.session_state.engine.generate_decision(sys_p, usr_p, docs)

# Decision Output Display with Audio Advisory
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    tab1, tab2, tab3, tab4 = st.tabs([T["tab1"], T["tab2"], T["tab3"], T["tab4"]])
    
    with tab1:
        st.subheader("Farm Health & Operational Risk Assessment")
        scores = result.get("risk_scores", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(T["crop_health"], f"{scores.get('crop_health', 75)}/100")
        c2.metric(T["weather_risk"], f"{scores.get('weather_risk', 20)}/100")
        c3.metric(T["pest_risk"], f"{scores.get('pest_risk', 30)}/100")
        c4.metric(T["market_risk"], f"{scores.get('market_risk', 40)}/100")
        
        status_summary = result.get("crop_status_summary", "")
        if status_summary:
            st.info(translate_text(status_summary, lang))
        
    with tab2:
        st.subheader(T["tab2"])
        raw_advice = result.get("actionable_decision", "")
        advice_text = translate_text(raw_advice, lang)
        st.write(advice_text)
        
        audio_stream = generate_audio(advice_text, lang)
        if audio_stream:
            st.audio(audio_stream, format="audio/mp3")
            
        sources = result.get("grounded_sources", [])
        if sources:
            st.caption(f"{T['sources']}: {', '.join(sources)}")
        
    with tab3:
        st.subheader(T["tab3"])
        for item in result.get("seven_day_plan", []):
            day_str = item.get("day", "")
            task_str = item.get("task", "")
            st.markdown(f"**{day_str}**: {translate_text(task_str, lang)}")
            
    with tab4:
        st.subheader(T["tab4"])
        sim = result.get("decision_simulation", {})
        if sim.get("option_a"):
            st.markdown(f"• **{T['opt_a']}:** {translate_text(sim.get('option_a'), lang)}")
        if sim.get("option_b"):
            st.markdown(f"• **{T['opt_b']}:** {translate_text(sim.get('option_b'), lang)}")
        if sim.get("selected"):
            st.success(f"{T['rec_choice']}: {translate_text(sim.get('selected'), lang)}")