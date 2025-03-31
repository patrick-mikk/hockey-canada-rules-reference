import streamlit as st
import json
import re

# Set page configuration
st.set_page_config(
    page_title="Hockey Canada Rules: Referee Quick Reference",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define Canada Red color
CANADA_RED = "#C8102E"

# Custom CSS for a more professional and compact layout
st.markdown(f"""
<style>
    /* Page background */
    .main-content {{
        background-color: #FFFFFF;
        padding: 1rem;
        max-width: 900px;
        margin: 0 auto;
    }}

    /* Header styles */
    .main-header {{
        background-color: {CANADA_RED};
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .main-header h1 {{
        margin: 0;
        font-size: 1.5rem;
    }}

    /* Rule card styling */
    .rule-card {{
        background-color: #fff;
        border: 1px solid #e0e0e0;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 0.5rem;
        margin-bottom: 0;
        transition: all 0.3s ease;
    }}
    
    .rule-header {{
        display: flex;
        justify-content: flex-start;
        align-items: center;
        margin-bottom: 0.2rem;
    }}
    
    .rule-number {{
        font-weight: 600;
        color: {CANADA_RED};
        font-size: 0.95rem;
        margin-right: 0.5rem;
        min-width: 2rem;
    }}
    
    .rule-title {{
        font-weight: 500;
        color: #333;
        font-size: 0.9rem;
    }}
    
    .rule-summary {{
        color: #666;
        font-size: 0.85rem;
        margin-bottom: 0;
        font-style: italic;
        margin-left: 2.5rem;
    }}
    
    /* Section styling */
    .section-header {{
        display: flex;
        align-items: center;
        margin: 0.5rem 0 0.3rem 0;
        padding: 0.3rem 0.5rem;
        background-color: {CANADA_RED};
        color: white;
        border-radius: 3px;
        font-size: 0.9rem;
    }}
    
    .section-icon {{
        margin-right: 0.3rem;
        font-size: 1rem;
    }}
    
    .section-title {{
        font-weight: 500;
        margin: 0;
        font-size: 0.9rem;
    }}
    
    /* Streamlit element overrides */
    .streamlit-expanderHeader {{
        font-size: 0.9rem !important;
        color: #666 !important;
        border-top-left-radius: 0 !important;
        border-top-right-radius: 0 !important;
        border-top: none !important;
        margin-top: 0 !important;
    }}
    .streamlit-expanderContent {{
        border-top: 1px solid #eee;
    }}
    
    /* Connect rule card with expander */
    .stExpander {{
        margin-top: 0 !important;
        border-top-left-radius: 0 !important;
        border-top-right-radius: 0 !important;
    }}
    
    /* Notes styling */
    .stAlert {{
        padding: 0.5rem !important;
        margin: 0.5rem 0 !important;
    }}
    
    /* Footer styling */
    .footer {{
        text-align: center;
        padding: 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid #eee;
        color: #999;
        font-size: 0.85rem;
    }}

    /* Rule list item styling */
    .rule-list-item {{
        margin-bottom: 0.8rem;
        padding-bottom: 0;
    }}
    
    hr {{
        margin: 0.5rem 0 !important;
        padding: 0 !important;
        border-top: 1px solid #eee !important;
        border-bottom: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Custom page header
st.markdown("""
<div class="main-header">
  <h1>Hockey Canada Rules</h1>
</div>
""", unsafe_allow_html=True)

# Helper function to get section from rule number
def get_section(rule_number):
    section_map = {
        "1": "PLAYING AREA",
        "2": "TEAMS",
        "3": "EQUIPMENT",
        "4": "TYPES OF PENALTIES",
        "5": "OFFICIALS",
        "6": "GAME FLOW",
        "7": "PHYSICAL FOULS",
        "8": "RESTRAINING FOULS",
        "9": "STICK FOULS",
        "10": "OTHER FOULS",
        "11": "MALTREATMENT"
    }
    section_num = rule_number.split('.')[0]
    return section_map.get(section_num, "OTHER")

# Helper function to get section icon
def get_section_icon(section):
    icons = {
        "PLAYING AREA": "🏟️",
        "TEAMS": "👥",
        "EQUIPMENT": "🏒",
        "TYPES OF PENALTIES": "⚠️",
        "OFFICIALS": "👮",
        "GAME FLOW": "⏱️",
        "PHYSICAL FOULS": "💥",
        "RESTRAINING FOULS": "🛑",
        "STICK FOULS": "🏑",
        "OTHER FOULS": "⚖️",
        "MALTREATMENT": "🚫"
    }
    return icons.get(section, "📖")

# Function to generate concise rule overviews
def get_rule_overview(rule):
    # Map of rule numbers to concise overviews
    rule_overviews = {
        # SECTION 1 - PLAYING AREA
        "1.1": "Defines the playing surface for ice hockey. Essential for understanding boundary lines and playing area limitations.",
        "1.2": "Standard rink dimensions: 200ft × 85-100ft with 28ft radius corners. Details boards (3ft 4in-4ft high), base plate, glass, and advertising restrictions.",
        "1.3": "Divides ice into attacking, neutral, and defending zones with specific markings. Includes goal lines (red), blue lines, and center red line positions and dimensions.",
        "1.4": "Goal posts must be 6ft apart, 4ft high, with proper net attachment. Includes specifications for net material, magnetic breakaway pegs, and red coloring requirements.",
        "1.5": "Goal crease is a 6ft radius semicircle with L-shaped markings at corners. Light blue interior with 2in wide red outline extending vertically to top of goal frame.",
        "1.6": "Center ice features a 12in blue spot with 15ft radius circle. Critical for face-offs and proper positioning of players during center ice play.",
        "1.7": "Neutral zone has two red face-off spots (2ft diameter) positioned 5ft from each blue line, with specific markings and dimensions for player positioning.",
        "1.8": "End zone face-off spots are positioned 22ft from center in each direction, 20ft from goal line. Includes detailed markings and positional requirements for players.",
        "1.9": "Players' bench must accommodate at least 14 players, positioned in neutral zone. Only uniformed players and 5 team officials permitted. Home team chooses ends.",
        "1.10": "Penalty benches must be separate from players' benches with sufficient seating. Must have separate penalty timekeeper area and direct access to ice.",
        "1.11": "Semi-circle with 10ft radius in front of timekeeper's bench. Officials use this area for consulting and rule discussions without player interference.",
        "1.12": "Rinks must have proper timing devices, goal lights, and signal systems. Includes requirements for automatic horn and light connections to game clock.",
        "1.13": "Teams must have separate, adequate dressing rooms with sanitary facilities. Officials require separate changing facilities for privacy and game preparation.",
        "1.14": "Rink lighting must be sufficient for players and spectators to clearly follow play. Critical for safety and proper game operation.",
        
        # SECTION 2 - TEAMS
        "2.1": "Teams consist of max 19 players (17 skaters + 2 goalies) and up to 5 team officials. Minimum requirement is 6 players to start/continue game. Details roles allowed on bench.",
        "2.2": "Players must be properly registered and appear on official game report. Includes rules on late arrivals, verification procedures, and penalties for ineligible players.",
        "2.3": "One captain and up to 2 alternates must be designated with 'C' and 'A' on jerseys. Only they may discuss rule interpretations with officials. Cannot dispute judgment calls.",
        "2.4": "Injured players (except goalies) must leave ice when play stops until play resumes. Refusal results in Delay of Game penalty. Includes special procedures for injured goalies.",
        
        # SECTION 3 - EQUIPMENT
        "3.1": "Officials can measure any equipment at any time. Illegal equipment results in Minor penalty; deliberately measuring own equipment prohibited (10-min Misconduct). Includes stick measurement process.",
        "3.2": "Players with broken/lost sticks must drop them immediately. Cannot receive stick thrown on ice (Minor penalty). Details procedures for retrieving replacement sticks from bench.",
        "3.3": "Player sticks: max length 63in, blade 12.5in × 3in. Junior/Senior players: curve limit 19mm. Includes material restrictions, tape allowances, and measurement procedures.",
        "3.4": "Skates must have CSA-approved safety guards and be designed for hockey. Goalie skates have specific blade width restrictions. Dangerous skates prohibited.",
        "3.5": "Comprehensive goalie equipment regulations including glove sizes (18in perimeter for catch glove), pad dimensions (11in width max), chest/arm protectors, and pants. Includes measurement procedures.",
        "3.6": "All players must wear CSA-approved helmet with chin strap, BNQ-certified full facial protection, protective gloves, etc. Junior/Senior leagues have specific visor requirements.",
        "3.7": "Equipment likely to cause injury is prohibited. Modified equipment that provides unfair advantage not allowed. Includes prohibition of electronic devices and non-standard alterations.",
        "3.8": "Standard puck: 1in thick, 3in diameter, weighing 5.5-6oz. Made of black vulcanized rubber. Frozen pucks must be available for games to maintain proper play characteristics.",
        "3.9": "Junior/Senior players must wear secure jersey tie-downs during fights. Penalty: Game Misconduct if jersey comes above shoulder blades or arm removed during fight. Applies even if tie-down breaks.",
        
        # SECTION 4 - TYPES OF PENALTIES
        "4.1": "Categorizes penalties: Minor (2min), Bench Minor, Major (5min), Misconduct (10min), Game Ejection, Game/Gross Misconduct, Match, and Penalty Shot. Details reporting requirements and official signals.",
        "4.2": "Minor penalty: 2 minutes, team plays shorthanded. Player returns if goal scored against team unless coincidental. Multiple minors served consecutively. Includes substitution rules.",
        "4.3": "Bench Minor: 2 minutes assessed to team not individual. Coach designates any non-penalized player to serve. Multiple bench minors served consecutively with different players serving each.",
        "4.4": "Major penalty: 5 minutes, team plays shorthanded for full duration regardless of goals scored. Results in automatic Game Misconduct in most cases. Includes substitution procedures.",
        "4.5": "When equal penalties to both teams, teams play at previous strength (4-on-4, etc.). Detailed rules for unequal coincidental penalties and order of penalty expiration.",
        "4.6": "Junior: coincidental Minor penalties result in immediate substitution at even strength. Penalties don't go on clock. Includes specific rules for multiple coincidental situations.",
        "4.7": "Misconduct: 10 minutes personal penalty, team plays at full strength. Second misconduct in same game results in automatic Game Misconduct. Penalties carry over between periods.",
        "4.8": "Game Ejection: removal from game, no time penalty. Game Misconduct: 10-min penalty to team plus player suspension. Automatic for 3 stick infractions, fighting, major penalties.",
        "4.9": "Gross Misconduct for extreme unsportsmanlike behavior (obscene gestures, discriminatory slurs, etc.). Results in player expulsion and minimum 1-game suspension.",
        "4.10": "Match penalty: 5-min time penalty plus player removal and suspension. For deliberate attempts to injure, excessive physical contact, or extreme rule violations.",
        "4.11": "Penalty Shot awarded for: breakaway fouls, player covering puck in crease, deliberate illegal substitution, displacing net during scoring chance, throwing objects at puck carrier, etc.",
        "4.12": "Goal awarded (without shot) when goalie removed and: player fouls opponent on breakaway, defensive player deliberately displaces net during scoring chance, or deliberately removes helmet.",
        "4.13": "Goalie penalties may be served by another player who was on ice when infraction occurred. Goalies never serve penalties themselves except Game/Gross Misconduct or Match penalties.",
        "4.14": "Delayed penalty called when offending team has possession. Play continues until offending team gains possession. Multiple delayed penalties have specific recording and timing procedures.",
        "4.15": "When calling penalties, referee signals infraction type and points to offending player. For major penalties, both arms extended. Linespersons can report certain infractions to referee.",
        
        # SECTION 5 - OFFICIALS
        "5.1": "Details appointment process for on-ice officials (referees/linespersons) and off-ice officials (timekeeper, scorer, etc.). Defines qualification requirements and equipment standards.",
        "5.2": "Referees have full authority before, during, and after games. Responsible for penalties, goals verification, and player safety. May overrule other officials and consult with linespeople.",
        "5.3": "Linespersons conduct face-offs, call icings, offsides, and can report major infractions to referee including high-sticking, butt-ending, and spearing. Details positioning responsibilities.",
        "5.4": "Goal judges positioned behind each net determine if puck completely crossed goal line. Can be consulted by referee but final decision rests with on-ice officials.",
        "5.5": "Penalty timekeeper records all penalties, maintains penalty bench, warns players when penalty time is about to expire (5 seconds), and reports violations of penalty bench rules.",
        "5.6": "Official scorer records goals, assists (max 2 per goal), penalties, and shots on goal. Responsible for official game report and verifying player eligibility before game starts.",
        "5.7": "Game timekeeper controls game clock, measures 15-minute intermissions and warm-up periods, signals end of periods, and notifies referee of timing disputes. Records all goals and assists.",
        
        # SECTION 6 - GAME FLOW
        "6.1": "Governs player substitutions during play (on-the-fly) and stoppages. Violations result in Bench Minor penalty. Includes detailed procedure for goaltender substitution and too many players.",
        "6.2": "Players must be properly positioned for face-offs: set sticks on ice, remain stationary, square stance. Violations result in player replacement. Details positioning for wingers and centers.",
        "6.3": "Specifies proper face-off locations after various stoppages: goals, penalties, offsides, etc. Generally at nearest spot that gives offending team least territorial advantage.",
        "6.4": "Junior/Senior: additional face-off location rules for defensive team icing, attacking team penalties, puck out of play in attacking zone, or goal dislodged by attacking team.",
        "6.5": "Junior: face-off violations (encroachment, alignment, premature movement) result in warnings, center replacement. Two violations by same team: Minor penalty.",
        "6.6": "Goal when entire puck crosses goal line. Disallowed if puck kicked/thrown in, scored with high stick, or after whistle/time expired. Assists: last two players touching puck.",
        "6.7": "Icing called when team shoots puck from behind center red line across opposing goal line. Resulting face-off in offending team's defensive zone. Includes hybrid icing rules.",
        "6.8": "If spectator interference occurs (physical contact, objects thrown), play stops immediately. Objects on ice: Bench Minor to home team. Details procedures for removing spectators.",
        "6.9": "High-sticking the puck above normal height (shoulder) results in stoppage unless played by opponent. Goal scored by high stick disallowed. Face-off at neutral zone.",
        "6.10": "Junior/Senior: playing puck above normal height is illegal. If done in defensive zone: face-off in that zone; if in neutral/attacking zone: neutral zone face-off.",
        "6.11": "Puck may be kicked anywhere except into goal. Deliberately kicking puck into goal disallowed. Deflecting off skate into goal is permitted if no distinct kicking motion.",
        "6.12": "Offside occurs when attacking players precede puck across blue line. Includes delayed offside procedure, intentional offside penalties, and proper face-off locations.",
        "6.13": "When puck goes out of play/becomes unplayable: face-off at nearest spot. Includes rules for puck on net, caught in netting, or lodged in/on boards. Details exceptions.",
        "6.14": "If puck can't be seen by referee or is illegal (broken), play stops. Foreign objects on ice cause immediate stoppage. Includes face-off location guidelines.",
        "6.15": "Play continues if puck hits official unless it goes into net directly off official or official is injured. Officials try to avoid interfering with play when possible.",
        "6.16": "Game starts with center ice face-off. Each period begins same way. Teams must start with correct number of players. Delay results in Bench Minor penalty.",
        "6.17": "Tied games may have overtime and/or shootout based on league rules. Details procedures for various overtime formats (5-on-5, 4-on-4, 3-on-3) and shootout requirements.",
        "6.18": "Three 20-minute periods in regulation with 15-minute intermissions (unless modified by league). Includes procedures for delays, timeouts, and clock operation.",
        
        # SECTION 7 - PHYSICAL FOULS
        "7.1": "Attempt to injure/deliberate injury results in Match penalty regardless of actual injury. Includes any deliberate action to cause harm. Automatic suspension. Serious violations reported to league.",
        "7.2": "Boarding (pushing/checking opponent violently into boards) results in Minor, Major+Game Misconduct, or Match penalty. Severity based on violence, intent, and injury. Focus on player safety.",
        "7.3": "Body-checking rules vary by age/division. Illegal in female hockey except Senior. Minor or Major+Game Misconduct. Legal checks must be with torso, never blindside, and opponent possessing puck.",
        "7.4": "Charging (taking 3+ strides before contact or excessive distance for check) penalized by Minor or Major+Game Misconduct. Charging goalie is always Major+Game Misconduct. Includes jumping.",
        "7.5": "Checking from behind (hit from behind into boards/net) results in Minor+Game Misconduct or Major+Game Misconduct. If violent/causes injury, Match penalty applies. Zero tolerance.",
        "7.6": "Head contact (intentional or reckless) results in Minor+Game Misconduct, Major+Game Misconduct, or Match penalty. Initial point of contact to head, neck, or face is key factor.",
        "7.7": "Junior/Senior: additional head contact provisions with stricter penalties. Direct head contact generally receives Major+Game Misconduct minimum. Includes detailed assessment criteria.",
        "7.8": "Kneeing (using knee to make contact with opponent) results in Minor, Major+Game Misconduct, or Match penalty. Severity based on intent and injury potential. Particularly dangerous to joints.",
        "7.9": "Roughing (pushing/shoving after whistle, face-washing, etc.) results in Minor penalty. Multiple roughing incidents can escalate to Major+Game Misconduct. Used for unnecessary rough play.",
        "7.10": "Fighting results in Major+Game Misconduct to all participants. Additional penalties for instigator/aggressor. Third-person in fight receives Game Misconduct. Includes multiple fight situations.",
        "7.11": "Instigator (starting fight) receives additional Minor. Aggressor (continuing fight with unwilling opponent) receives additional Minor + Game Misconduct. Defined by who throws first punch, verbal instigation, etc.",
        
        # SECTION 8 - RESTRAINING FOULS
        "8.1": "Holding (impeding opponent's movement with hands, arms, legs) results in Minor penalty. Includes grabbing jersey/equipment, bear hugs, and pinning against boards. Key aspect: restricting free movement.",
        "8.2": "Hooking (impeding progress using stick against body/stick) results in Minor penalty. If hooking prevents clear scoring chance: Penalty Shot. If injury results: Major+Game Misconduct.",
        "8.3": "Interference (impeding player without puck possession) results in Minor penalty. Includes picking, screening, free hand restraints. Exception: player may block path when seeking position.",
        "8.4": "Interference from bench (holding/interfering with opponent from player/penalty bench) results in Bench Minor or Major+Game Misconduct. Physical contact with player on ice is automatic Major+Game Misconduct.",
        "8.5": "Interference with goaltender (preventing movement in crease, contact when establishing position) results in Minor penalty. Goals disallowed when goalie impeded. Includes contact criteria.",
        "8.6": "Tripping (using stick/any body part to cause opponent to fall) results in Minor penalty. Accidental trips on breakaways result in Penalty Shot. Injury from tripping: Major+Game Misconduct.",
        "8.7": "Clipping (hitting at/below knees) results in Minor, Major+Game Misconduct, or Match penalty. Severity based on intent and impact. Particularly dangerous action due to knee injury risk.",
        "8.8": "Slew-footing (kicking feet out from behind causing backward fall) results in Major+Game Misconduct or Match penalty. One of the most dangerous actions in hockey due to head injury risk.",
        
        # SECTION 9 - STICK FOULS
        "9.1": "Butt-ending (jabbing opponent with stick handle end) results in Double Minor+Game Misconduct or Major+Game Misconduct. Even attempt receives Double Minor+Game Misconduct. Serious potential for injury.",
        "9.2": "Cross-checking (checking with stick shaft while both hands on stick) results in Minor, Major+Game Misconduct, or Match penalty based on force/injury. Common in front of net battles.",
        "9.3": "Slashing (swinging stick at opponent) results in Minor, Major+Game Misconduct, or Match penalty. Includes stick contact on/near hands and non-puck contact. Tapping stick not normally penalized.",
        "9.4": "Spearing (stabbing opponent with stick blade tip) results in Double Minor+Game Misconduct or Major+Game Misconduct. Even attempt receives Double Minor+Game Misconduct. Very dangerous action.",
        "9.5": "Junior/Senior: high-sticking (stick above shoulder contacting opponent) receives Minor, Double Minor (if injury), Major+Game Misconduct, or Match penalty depending on severity and blood drawn.",
        
        # SECTION 10 - OTHER FOULS
        "10.1": "Delay of Game: deliberately displacing net (Minor/Penalty Shot), freezing puck unnecessarily (Minor), falling on puck (Minor), adjustment of equipment during play (Minor). Goalie freezing puck outside crease: Minor.",
        "10.2": "Diving/embellishment to draw penalty results in Minor penalty. Can be called in addition to legitimate penalty on opponent. Example: exaggerating fall on trip. Undermines game integrity.",
        "10.3": "Hand pass allowed in defensive zone only. Closing hand on puck: Minor penalty. Picking up puck in crease by defending player: Penalty Shot. If goalie removed: Awarded Goal.",
        "10.4": "Players/officials leaving bench inappropriately: Minor, Major+Game Misconduct, or Gross Misconduct. First player off bench during altercation: additional Game Misconduct + minimum 5-game suspension.",
        "10.5": "Throwing stick/object at puck/player in defending zone: Penalty Shot. In neutral/attacking zone: Minor. At official: Match penalty. If goalie removed and thrown at puck: Awarded Goal.",
        "10.6": "Playing with broken stick prohibited: Minor penalty. Picking up another player's stick or receiving stick incorrectly: Minor penalty. Identifies what constitutes 'broken' stick.",
        "10.7": "Premature goaltender substitution (too many players) results in face-off at center ice. No penalty if for delayed penalty, but no play allowed by extra attacker before referee's signal.",
        "10.8": "Refusing to start play after warning: Minor penalty. Continued refusal: Major+Game Misconduct. Leaving ice to protest call: Major+Game Misconduct. Can result in forfeit of game.",
        "10.9": "Removing helmet before fight (player's own or opponent's) results in Minor penalty. Intent is to discourage fighting and increase player safety by maintaining head protection.",
        "10.10": "Junior/Senior: players leaving feet to play puck on goal netting receive Minor penalty. Preventative rule to avoid dangerous plays near boards and potential injuries from falling.",
        
        # SECTION 11 - MALTREATMENT
        "11.1": "Unsportsmanlike conduct (disrespect, intimidation, etc.) results in Minor, Misconduct, Game Misconduct or Match penalty. Includes inappropriate language/gestures, diving, inciting, and excessive celebration.",
        "11.2": "Disrespecting officials verbally or through gestures results in Misconduct, Game Misconduct, or Gross Misconduct. Includes disputing calls, post-game incidents, and verbal abuse. Automatic suspension.",
        "11.3": "Discriminatory slurs/taunts based on race, ethnic origin, religion, gender, sexual orientation, etc. result in Gross Misconduct and minimum 5-game suspension. Zero tolerance policy.",
        "11.4": "Physical harassment of officials results in Match penalty and suspension. Categories range from threatening gestures (Category I: min. 6 games) to deliberate physical force (Category III: min. 1 year).",
        "11.5": "Spitting at/on opponents, officials, or spectators results in Match penalty and automatic suspension. Includes any deliberate expulsion of bodily fluid at another person. Serious health and respect violation."
    }
    
    # Return the overview if available, otherwise create a generic one
    base_rule_num = rule["number"].split(" ")[0]
    if base_rule_num in rule_overviews:
        return rule_overviews[base_rule_num]
    else:
        return f"Covers rules relating to {rule['title']}."

# Load the data
@st.cache_data
def load_data():
    with open("output/rulebook.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    section_order = {
        "PLAYING AREA": 1,
        "TEAMS": 2,
        "EQUIPMENT": 3,
        "TYPES OF PENALTIES": 4,
        "OFFICIALS": 5,
        "GAME FLOW": 6,
        "PHYSICAL FOULS": 7,
        "RESTRAINING FOULS": 8,
        "STICK FOULS": 9,
        "OTHER FOULS": 10,
        "MALTREATMENT": 11
    }
    
    return data["rule"], section_order

rules, section_order = load_data()

# Sidebar with search and filters
with st.sidebar:
    # Search
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    
    st.subheader("🔍 Search Rules")
    search_input = st.text_input(
        "Search",
        value=st.session_state["search_query"],
        label_visibility="collapsed",
        placeholder="Search for rules..."
    )
    st.session_state["search_query"] = search_input

    # Clear search button
    if st.button("Clear Search", key="clear_btn"):
        st.session_state["search_query"] = ""
        st.rerun()

    # Section filters
    st.subheader("Sections")
    all_sections = sorted(set(get_section(rule["number"]) for rule in rules))
    all_sections_sorted = sorted(all_sections, key=lambda s: section_order.get(s, 9999))

    select_all = st.checkbox("Select All", value=True, key="select_all")
    
    selected_sections = []
    for sec in all_sections_sorted:
        checked = st.checkbox(f"{get_section_icon(sec)} {sec}", value=select_all, key=f"cb_{sec}")
        if checked:
            selected_sections.append(sec)

# Main content container
with st.container():
    # Filter rules
    search_query = st.session_state["search_query"].lower()
    filtered_rules = rules

    if search_query:
        filtered_rules = [
            rule for rule in rules
            if search_query in rule["number"].lower() or
               search_query in rule["title"].lower() or
               search_query in rule["text"].lower() or
               any(search_query in note.lower() for note in rule["notes"]) or
               any(search_query in sub["text"].lower() for sub in rule["subsection"])
        ]
        st.write(f"Found {len(filtered_rules)} rules matching: '{search_query}'")

    if selected_sections:
        filtered_rules = [
            rule for rule in filtered_rules
            if get_section(rule["number"]) in selected_sections
        ]

    # Group and sort rules
    section_rules = {}
    for rule in filtered_rules:
        section = get_section(rule["number"])
        if section not in section_rules:
            section_rules[section] = []
        section_rules[section].append(rule)

    for section in section_rules:
        section_rules[section].sort(key=lambda x: [int(n) for n in x["number"].split('.')])

    # Display rules in list format
    for section in sorted(section_rules.keys(), key=lambda s: section_order.get(s, 9999)):
        section_rules_list = section_rules[section]
        if not section_rules_list:
            continue

        section_icon = get_section_icon(section)
        st.markdown(f'<div class="section-header"><span class="section-icon">{section_icon}</span><span class="section-title">{section}</span></div>', unsafe_allow_html=True)

        # Display each rule as a list item
        for rule in section_rules_list:
            # Get the concise overview for this rule
            overview = get_rule_overview(rule)

            # Create rule header and summary
            st.markdown(f'''
                <div class="rule-list-item">
                    <div class="rule-card">
                        <div class="rule-header">
                            <span class="rule-number">{rule["number"]}</span>
                            <span class="rule-title">{rule["title"]}</span>
                        </div>
                        <div class="rule-summary">{overview}</div>
                    </div>
            ''', unsafe_allow_html=True)
            
            # Use Streamlit's native expander for details without any gap
            with st.expander("View Details"):
                # Main rule text
                if rule["text"]:
                    st.write(rule["text"])
                
                # Notes section
                if rule["notes"]:
                    for note in rule["notes"]:
                        st.info(note)
                
                # Subsections
                if rule["subsection"]:
                    for sub in rule["subsection"]:
                        st.markdown(f"**{sub['number']}**: {sub['text']}")
            
            # Add divider after the expander
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Close the rule list item div
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
  © 2025 Patrick A. Mikkelsen · Powered by Streamlit
</div>
""", unsafe_allow_html=True)
