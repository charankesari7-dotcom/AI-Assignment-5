"""
planner.py
----------
AI-Based Travel Planner
Author: Student Submission

This planner uses in-memory knowledge bases (simulating ontologies)
for Tourist Places, Food Recommendations, and Cost Estimation.
It generates a personalized tour plan based on user preferences.

Architecture:
  User Input → Preference Filter → Knowledge Base Query
             → Tour Plan Generator → Cost Estimator → Output
"""

# ─── Knowledge Bases (simulating ontology/RDF data) ───────────────────────────

TOURIST_PLACES = {
    "Goa": {
        "type": ["beach", "nightlife", "heritage"],
        "best_season": ["October", "November", "December", "January", "February"],
        "avg_daily_cost_inr": 3000,
        "attractions": ["Calangute Beach", "Baga Beach", "Old Goa Churches", "Dudhsagar Falls"],
        "rating": 4.5,
    },
    "Manali": {
        "type": ["mountains", "adventure", "nature"],
        "best_season": ["May", "June", "October"],
        "avg_daily_cost_inr": 2500,
        "attractions": ["Rohtang Pass", "Solang Valley", "Hadimba Temple", "Old Manali"],
        "rating": 4.6,
    },
    "Jaipur": {
        "type": ["heritage", "culture", "architecture"],
        "best_season": ["October", "November", "December", "January", "February", "March"],
        "avg_daily_cost_inr": 2000,
        "attractions": ["Amber Fort", "Hawa Mahal", "City Palace", "Jantar Mantar"],
        "rating": 4.4,
    },
    "Munnar": {
        "type": ["nature", "tea gardens", "trekking"],
        "best_season": ["September", "October", "November", "March", "April", "May"],
        "avg_daily_cost_inr": 2200,
        "attractions": ["Tea Plantations", "Eravikulam National Park", "Mattupetty Dam"],
        "rating": 4.5,
    },
    "Varanasi": {
        "type": ["spiritual", "culture", "heritage"],
        "best_season": ["October", "November", "December", "January", "February", "March"],
        "avg_daily_cost_inr": 1800,
        "attractions": ["Dashashwamedh Ghat", "Kashi Vishwanath Temple", "Sarnath"],
        "rating": 4.3,
    },
}

FOOD_RECOMMENDATIONS = {
    "Goa": ["Fish Curry Rice", "Prawn Balchão", "Bebinca", "Feni Cocktails"],
    "Manali": ["Siddu", "Dham", "Babru", "Aktori"],
    "Jaipur": ["Dal Baati Churma", "Ghewar", "Laal Maas", "Pyaaz Kachori"],
    "Munnar": ["Puttu & Kadala Curry", "Appam with Stew", "Tapioca", "Kerala Sadya"],
    "Varanasi": ["Kachori Sabzi", "Lassi", "Malaiyo", "Chaat"],
}

ACCOMMODATION = {
    "budget": {"cost_per_night_inr": 800, "label": "Hostel / Budget Guesthouse"},
    "mid":    {"cost_per_night_inr": 2500, "label": "3-star Hotel"},
    "luxury": {"cost_per_night_inr": 7000, "label": "5-star Resort"},
}

TRANSPORT_COST_INR = {
    "bus":    500,
    "train":  1000,
    "flight": 4000,
}


# ─── Planner Logic ────────────────────────────────────────────────────────────

def filter_destinations(interests, month, budget_tier):
    """
    Filter tourist places based on user interests, travel month,
    and whether the cost fits a rough budget tier.

    Budget tiers: 'low' (< 2200 INR/day), 'medium' (2200–4000), 'high' (>4000)

    Returns a sorted list of (place_name, place_data) tuples.
    """
    budget_limits = {"low": 2200, "medium": 4000, "high": float("inf")}
    max_cost = budget_limits.get(budget_tier, float("inf"))

    matched = []
    for name, data in TOURIST_PLACES.items():
        # Check if month is suitable
        if month not in data["best_season"]:
            continue
        # Check if any interest matches place type
        if not any(interest in data["type"] for interest in interests):
            continue
        # Check budget fit
        if data["avg_daily_cost_inr"] > max_cost:
            continue
        matched.append((name, data))

    # Sort by rating descending
    matched.sort(key=lambda x: x[1]["rating"], reverse=True)
    return matched


def estimate_cost(destination, days, accommodation_tier, transport_mode):
    """
    Estimate total trip cost in INR.

    Parameters
    ----------
    destination       : name of the place (string)
    days              : number of days
    accommodation_tier: 'budget', 'mid', 'luxury'
    transport_mode    : 'bus', 'train', 'flight'

    Returns
    -------
    breakdown : dict with per-category costs
    total     : int, total estimated cost
    """
    place = TOURIST_PLACES.get(destination, {})
    daily_cost = place.get("avg_daily_cost_inr", 2000)
    night_cost = ACCOMMODATION[accommodation_tier]["cost_per_night_inr"]
    transport  = TRANSPORT_COST_INR[transport_mode]

    breakdown = {
        "Daily Activities & Food (INR)": daily_cost * days,
        "Accommodation (INR)":           night_cost * days,
        "Transport (to & fro) (INR)":    transport * 2,
    }
    total = sum(breakdown.values())
    return breakdown, total


def build_itinerary(destination, days):
    """
    Build a simple day-by-day itinerary from the attraction list.
    """
    place = TOURIST_PLACES.get(destination, {})
    attractions = place.get("attractions", [])
    food_list = FOOD_RECOMMENDATIONS.get(destination, [])

    itinerary = []
    for day in range(1, days + 1):
        # Rotate through attractions
        attraction = attractions[(day - 1) % len(attractions)] if attractions else "Free Exploration"
        food = food_list[(day - 1) % len(food_list)] if food_list else "Local cuisine"
        itinerary.append({
            "day": day,
            "activity": attraction,
            "recommended_food": food,
        })
    return itinerary


def generate_tour_plan(name, interests, month, days, budget_tier,
                        accommodation_tier, transport_mode):
    """
    Main entry point: generate a complete personalised tour plan.

    Parameters
    ----------
    name               : traveller's name
    interests          : list of strings (e.g. ['beach', 'nature'])
    month              : travel month (e.g. 'November')
    days               : number of travel days
    budget_tier        : 'low', 'medium', or 'high'
    accommodation_tier : 'budget', 'mid', or 'luxury'
    transport_mode     : 'bus', 'train', or 'flight'

    Returns
    -------
    plan : dict containing destination, itinerary, cost breakdown, total cost
    """
    matched = filter_destinations(interests, month, budget_tier)

    if not matched:
        return {"error": "No matching destination found for given preferences."}

    # Pick the top-rated matching destination
    top_dest, top_data = matched[0]

    itinerary = build_itinerary(top_dest, days)
    breakdown, total = estimate_cost(top_dest, days, accommodation_tier, transport_mode)

    plan = {
        "traveller": name,
        "destination": top_dest,
        "type": top_data["type"],
        "rating": top_data["rating"],
        "month": month,
        "days": days,
        "accommodation": ACCOMMODATION[accommodation_tier]["label"],
        "transport": transport_mode,
        "itinerary": itinerary,
        "cost_breakdown": breakdown,
        "total_cost_inr": total,
        "food_specialties": FOOD_RECOMMENDATIONS.get(top_dest, []),
        "other_options": [name for name, _ in matched[1:]],
    }
    return plan


def print_plan(plan):
    """Pretty-print the tour plan."""
    if "error" in plan:
        print(f"Error: {plan['error']}")
        return

    print("=" * 60)
    print(f"  PERSONALISED TOUR PLAN FOR: {plan['traveller']}")
    print("=" * 60)
    print(f"  Destination  : {plan['destination']}")
    print(f"  Type         : {', '.join(plan['type'])}")
    print(f"  Rating       : {plan['rating']} / 5.0")
    print(f"  Month        : {plan['month']}")
    print(f"  Duration     : {plan['days']} days")
    print(f"  Stay         : {plan['accommodation']}")
    print(f"  Transport    : {plan['transport']}")
    print()
    print("  ITINERARY:")
    for entry in plan["itinerary"]:
        print(f"    Day {entry['day']}: Visit {entry['activity']}")
        print(f"           Try: {entry['recommended_food']}")
    print()
    print("  FOOD SPECIALTIES:")
    for food in plan["food_specialties"]:
        print(f"    - {food}")
    print()
    print("  COST BREAKDOWN:")
    for k, v in plan["cost_breakdown"].items():
        print(f"    {k}: ₹{v:,}")
    print(f"  TOTAL ESTIMATED COST: ₹{plan['total_cost_inr']:,}")
    print()
    if plan["other_options"]:
        print(f"  Other matching destinations: {', '.join(plan['other_options'])}")
    print("=" * 60)


# ─── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    plan = generate_tour_plan(
        name="Arjun",
        interests=["beach", "nature"],
        month="November",
        days=5,
        budget_tier="medium",
        accommodation_tier="mid",
        transport_mode="flight"
    )
    print_plan(plan)
