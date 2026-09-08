import datetime
from models import SessionLocal, StandardRecord, init_db

MOCK_DATA = [
    {
        "is_number": "IS 2347:2017",
        "title": "Domestic Pressure Cookers - Specification",
        "scope": "This standard covers the requirements for domestic pressure cookers. It specifies the materials, construction, and performance requirements.",
        "product_category": "Kitchen Appliances",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Bursting pressure test, operating pressure test, proof pressure test.",
        "lab_info": "Various BIS-approved labs nationwide",
        "url": "https://www.bis.gov.in/product/is-2347/",
        "last_updated": datetime.date(2017, 5, 12)
    },
    {
        "is_number": "IS 302-2-15:2009",
        "title": "Safety of Household and Similar Electrical Appliances - Particular Requirements for Appliances for Heating Liquids",
        "scope": "Covers electric kettles, coffee makers, and similar appliances for heating liquids.",
        "product_category": "Electrical Appliances",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Electric strength test, leakage current test, heating test.",
        "lab_info": "National Test House (NTH), ERTL",
        "url": "https://www.bis.gov.in/product/is-302-2-15/",
        "last_updated": datetime.date(2009, 8, 20)
    },
    {
        "is_number": "IS 14534:1998",
        "title": "Plastics - Guidelines for the Recovery and Recycling of Plastics Waste",
        "scope": "Guidelines for recovery and recycling of plastic waste.",
        "product_category": "Environment & Plastics",
        "certification_scheme": "Voluntary Certification",
        "testing_requirements": "Material identification, contamination level checks.",
        "lab_info": "CIPET (Central Institute of Plastics Engineering & Technology)",
        "url": "https://www.bis.gov.in/product/is-14534/",
        "last_updated": datetime.date(1998, 11, 5)
    },
    {
        "is_number": "IS 15822:2006",
        "title": "Stainless Steel Utensils - Specification",
        "scope": "Specifies requirements for domestic stainless steel utensils.",
        "product_category": "Kitchenware",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Material composition (Grade 304/200 series), corrosion resistance, thickness.",
        "lab_info": "National Metallurgical Laboratory",
        "url": "https://www.bis.gov.in/product/is-15822/",
        "last_updated": datetime.date(2006, 2, 14)
    },
    {
        "is_number": "IS 14155:1994",
        "title": "Domestic Gas Stoves for use with Liquefied Petroleum Gases",
        "scope": "Covers safety and performance of LPG gas stoves.",
        "product_category": "Kitchen Appliances",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Thermal efficiency, gas leakage test, combustion test.",
        "lab_info": "IIP (Indian Institute of Petroleum)",
        "url": "https://www.bis.gov.in/product/is-14155/",
        "last_updated": datetime.date(1994, 6, 30)
    },
    {
        "is_number": "IS 1293:2019",
        "title": "Plugs and Socket-Outlets of Rated Voltage up to and including 250 V and Rated Current up to and including 16 A",
        "scope": "Requirements for plugs and socket-outlets for household electrical purposes.",
        "product_category": "Electrical Accessories",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Contact resistance, breaking capacity, normal operation test.",
        "lab_info": "CPRI (Central Power Research Institute)",
        "url": "https://www.bis.gov.in/product/is-1293/",
        "last_updated": datetime.date(2019, 10, 15)
    },
    {
        "is_number": "IS 1554-1:1988",
        "title": "PVC insulated (heavy duty) electric cables: Part 1 for working voltages up to and including 1100 V",
        "scope": "Specifies PVC cables for heavy duty electrical applications.",
        "product_category": "Electrical Cables",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Conductor resistance, insulation thickness, flammability test.",
        "lab_info": "CPRI, ERDA",
        "url": "https://www.bis.gov.in/product/is-1554-1/",
        "last_updated": datetime.date(1988, 3, 21)
    },
    {
        "is_number": "IS 8144:2018",
        "title": "Multipurpose Dry Batteries - Specification",
        "scope": "Requirements for non-rechargeable dry cell batteries (AA, AAA, etc.).",
        "product_category": "Batteries",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Discharge test, leakage test, open circuit voltage.",
        "lab_info": "NTH, ETDC",
        "url": "https://www.bis.gov.in/product/is-8144/",
        "last_updated": datetime.date(2018, 7, 10)
    },
    {
        "is_number": "IS 16046:2015",
        "title": "Secondary Cells and Batteries containing Alkaline or other non-acid Electrolytes",
        "scope": "Safety requirements for portable sealed secondary cells.",
        "product_category": "Batteries",
        "certification_scheme": "CRS (Compulsory Registration Scheme)",
        "testing_requirements": "Continuous low-rate charge, vibration, temperature cycling, short circuit.",
        "lab_info": "UL India, TUV Rheinland",
        "url": "https://www.bis.gov.in/product/is-16046/",
        "last_updated": datetime.date(2015, 9, 25)
    },
    {
        "is_number": "IS 14220:1994",
        "title": "Open Pan Sugar (Khandsari) - Specification",
        "scope": "Specification for Khandsari sugar produced by open pan process.",
        "product_category": "Food & Agriculture",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Moisture content, polarization, colour, sulphur dioxide content.",
        "lab_info": "NSI (National Sugar Institute)",
        "url": "https://www.bis.gov.in/product/is-14220/",
        "last_updated": datetime.date(1994, 12, 1)
    },
    {
        "is_number": "IS 13428:2005",
        "title": "Packaged Natural Mineral Water - Specification",
        "scope": "Specifies requirements for packaged natural mineral water.",
        "product_category": "Food & Beverages",
        "certification_scheme": "Scheme I (ISI Mark) - Mandatory",
        "testing_requirements": "Microbiological tests, heavy metals, radioactive residues.",
        "lab_info": "Various NABL and BIS recognized labs",
        "url": "https://www.bis.gov.in/product/is-13428/",
        "last_updated": datetime.date(2005, 4, 18)
    },
    {
        "is_number": "IS 14543:2016",
        "title": "Packaged Drinking Water (Other than Packaged Natural Mineral Water)",
        "scope": "Requirements for packaged drinking water.",
        "product_category": "Food & Beverages",
        "certification_scheme": "Scheme I (ISI Mark) - Mandatory",
        "testing_requirements": "pH, TDS, microbiological parameters, pesticide residues.",
        "lab_info": "CFL (Central Food Laboratory)",
        "url": "https://www.bis.gov.in/product/is-14543/",
        "last_updated": datetime.date(2016, 6, 22)
    },
    {
        "is_number": "IS 15298-2:2016",
        "title": "Personal Protective Equipment - Part 2 Safety Footwear",
        "scope": "Requirements for safety footwear for industrial use.",
        "product_category": "Personal Protective Equipment",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Impact resistance of toe cap, slip resistance, ergonomic features.",
        "lab_info": "FDDI (Footwear Design and Development Institute)",
        "url": "https://www.bis.gov.in/product/is-15298-2/",
        "last_updated": datetime.date(2016, 11, 8)
    },
    {
        "is_number": "IS 299:2012",
        "title": "Alumino-ferric - Specification",
        "scope": "Requirements for alumino-ferric used in water purification.",
        "product_category": "Chemicals",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Alumina content, iron content, insoluble matter.",
        "lab_info": "Various chemical testing labs",
        "url": "https://www.bis.gov.in/product/is-299/",
        "last_updated": datetime.date(2012, 1, 15)
    },
    {
        "is_number": "IS 14625:2015",
        "title": "Hallmarking of Gold Jewellery/Artefacts - Guidelines",
        "scope": "Guidelines for operating assaying and hallmarking centres for gold.",
        "product_category": "Hallmarking",
        "certification_scheme": "Hallmarking Scheme",
        "testing_requirements": "XRF analysis, fire assay test.",
        "lab_info": "BIS Recognized Assaying and Hallmarking Centres",
        "url": "https://www.bis.gov.in/product/is-14625/",
        "last_updated": datetime.date(2015, 8, 30)
    },
    {
        "is_number": "IS 2112:2014",
        "title": "Hallmarking of Silver Jewellery/Artefacts - Guidelines",
        "scope": "Guidelines for operating assaying and hallmarking centres for silver.",
        "product_category": "Hallmarking",
        "certification_scheme": "Hallmarking Scheme",
        "testing_requirements": "Potentiometric titration, XRF.",
        "lab_info": "BIS Recognized Assaying and Hallmarking Centres",
        "url": "https://www.bis.gov.in/product/is-2112/",
        "last_updated": datetime.date(2014, 12, 10)
    },
    {
        "is_number": "IS 15410:2003",
        "title": "Containers for Packaging of Packaged Drinking Water and Packaged Natural Mineral Water",
        "scope": "Specifies requirements for plastic containers for drinking water.",
        "product_category": "Packaging",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Migration limits, overall drop test, stackability.",
        "lab_info": "IIP (Indian Institute of Packaging)",
        "url": "https://www.bis.gov.in/product/is-15410/",
        "last_updated": datetime.date(2003, 3, 22)
    },
    {
        "is_number": "IS 2082:1993",
        "title": "Stationary Storage Type Electric Water Heaters",
        "scope": "Specifies requirements for stationary storage type electric water heaters (geysers).",
        "product_category": "Electrical Appliances",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Insulation resistance, thermostat operation, hydraulic pressure test.",
        "lab_info": "CPRI, NTH",
        "url": "https://www.bis.gov.in/product/is-2082/",
        "last_updated": datetime.date(1993, 10, 5)
    },
    {
        "is_number": "IS 3854:1997",
        "title": "Switches for Domestic and Similar Purposes",
        "scope": "Requirements for general purpose electrical switches.",
        "product_category": "Electrical Accessories",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Making and breaking capacity, temperature rise, endurance test.",
        "lab_info": "ERDA, CPRI",
        "url": "https://www.bis.gov.in/product/is-3854/",
        "last_updated": datetime.date(1997, 5, 20)
    },
    {
        "is_number": "IS 17017-1:2018",
        "title": "Electric Vehicle Conductive AC Charging System - Part 1: General Requirements",
        "scope": "Specifies general requirements for EV AC charging stations.",
        "product_category": "Automotive & EV",
        "certification_scheme": "Scheme I (ISI Mark)",
        "testing_requirements": "Dielectric withstand voltage, touch current, ingress protection (IP).",
        "lab_info": "ARAI, ICAT",
        "url": "https://www.bis.gov.in/product/is-17017-1/",
        "last_updated": datetime.date(2018, 11, 25)
    }
]

def seed_database():
    init_db()
    session = SessionLocal()
    
    # Check if data already exists
    if session.query(StandardRecord).first():
        print("Database already contains data. Skipping seed.")
        session.close()
        return

    for item in MOCK_DATA:
        record = StandardRecord(**item)
        session.add(record)
    
    session.commit()
    session.close()
    print(f"Successfully seeded {len(MOCK_DATA)} records into the database.")

if __name__ == "__main__":
    seed_database()
