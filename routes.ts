// lib/routes.ts

// ---------------------------------------------------------
// Detailed route pages (for /routes/[slug])
// ---------------------------------------------------------

export type RouteDetailSlug =
  | "nicosia-larnaca-airport"
  | "nicosia-test-destination"
  | "nicosia-troodos"
  | "nicosia-limassol"
  | "nicosia-paphos-airport"
  | "nicosia-ercan-airport"
  | "paphos-airport-nicosia"
  | "paphos-airport-limassol"
  | "paphos-airport-larnaca"
  | "paphos-airport-ayia-napa"
  | "paphos-airport-ercan-airport"
  | "larnaca-airport-famagusta"
  | "larnaca-airport-kyrenia"
  | "larnaca-airport-limassol"
  | "larnaca-airport-nicosia"
  | "larnaca-airport-paphos"
  | "limassol-ercan-airport"
  | "limassol-nicosia"
  | "limassol-paphos-airport"
  | "limassol-paphos"
  | "limassol-troodos";

export type RouteFAQ = {
  question: string;
  answer: string;
};

export type VehicleOption = {
  type: string;
  maxPassengers: string;
  idealFor: string;
  fixedPrice: string;
};

export type RouteDetail = {
  // 👇 NEW: link to booking routes
  bookingRouteId?: string;

  slug: RouteDetailSlug;
  from: string;
  to: string;

  metaTitle: string;
  metaDescription: string;

  heroTitle: string;
  subheadline: string;

  body: string;

  distance: string;
  time: string;
  sedanPrice: string;
  vanPrice: string;

  whatMakesBetter?: string[];
  whatsIncluded: string[];
  vehicleOptions: VehicleOption[];
  destinationHighlights?: string[];
  idealFor?: string[];

  faq: RouteFAQ[];

  image: string;
  bookHref: string;
  bookCtaLabel: string;
  bookCtaSupport: string;
};

export const ROUTE_DETAILS: RouteDetail[] = [
  // 1) Nicosia → Larnaca Airport (LCA)
  {
    slug: "nicosia-larnaca-airport",
    from: "Nicosia",
    to: "Larnaca Airport (LCA)",

    metaTitle:
      "Taxi from Nicosia to Larnaca Airport (LCA) | Fixed-Price Private Transfer",
    metaDescription:
      "Private taxi from Nicosia to Larnaca Airport at a fixed price: €55 for up to 4 passengers or €80 for up to 6. No hidden surcharges. 24/7 service, flight-safe timing, Wi-Fi and bottled water. Ideal for early and late departures.",

    heroTitle: "Taxi Transfer from Nicosia to Larnaca Airport (LCA)",
    subheadline:
      "Fixed Prices: €55 (up to 4 passengers) · €80 (up to 6 passengers)\nDistance: ~52–60 km · Average Journey: 40–50 minutes",

    body: `Need to catch a flight from Larnaca Airport (LCA) while you’re staying in Nicosia? Our private taxi transfer from Nicosia to Larnaca Airport offers a safe, punctual and stress-free solution with a clear, fixed price.

For a fixed fare of €55 per car (up to 4 passengers) or €80 per minivan (up to 6 passengers), your driver will collect you from any address in Nicosia – home, hotel, office, embassy, university – help with your luggage and drive you directly to the departures terminal at Larnaca Airport.

We plan pickup times around your flight, taking into account traffic, check-in and airline recommendations, so you arrive on time without rushing. All vehicles are modern, air-conditioned and equipped with free Wi-Fi and bottled water, so you can relax or finish last-minute work on the way.`,

    distance: "52–60 km",
    time: "40–50 minutes",
    sedanPrice: "€55",
    vanPrice: "€80",

    whatMakesBetter: [
      "Fixed prices: €55 (1–4 passengers) · €80 (up to 6 passengers)",
      "No hidden surcharges same fare day & night",
      "Pickup from anywhere in Nicosia (city centre, Engomi, Strovolos, etc.)",
      "Drivers used to airport timings and peak hours",
      "24/7 availability for early morning or late-night flights",
      "Perfect for business travellers, families, students and groups",
    ],

    whatsIncluded: [
      "€55 per standard car (up to 4 passengers)",
      "€80 per minivan (up to 6 passengers)",
      "Door-to-door pickup at any Nicosia address",
      "Drop-off at Larnaca Airport (LCA) departures",
      "Free Wi-Fi & bottled water in every vehicle",
      "Child / baby seats on request (no extra fee)",
      "Licensed, insured, English-speaking driver",
      "All tolls, VAT and insurance included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Business travellers, couples, small families",
        fixedPrice: "€55",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, groups, extra luggage",
        fixedPrice: "€80",
      },
    ],

    destinationHighlights: [
      "Larnaca Airport is the main international hub for flights to and from Cyprus.",
      "A pre-booked taxi from Nicosia gives you a guaranteed arrival time, planned around your flight.",
      "No parking, no bus changes, no luggage dragging.",
      "A comfortable, private start or end to your trip.",
    ],

    idealFor: [
      "Families and groups travelling with luggage",
      "Business travellers and conference guests",
      "Students and expats flying in and out of Cyprus",
      "Anyone who prefers a direct, private transfer instead of buses or multiple taxis",
    ],

    faq: [
      {
        question: "Is €65 per person or per car?",
        answer:
          "It’s per car, up to 4 passengers. For up to 6 passengers, the fixed minivan price is €80 per vehicle.",
      },
      {
        question: "How early will you pick us up before our flight?",
        answer:
          "Normally around 3 hours before departure (or more in high season), adjusted to your airline’s check-in guidelines and traffic conditions.",
      },
      {
        question: "Can I get an invoice for my company?",
        answer:
          "Yes. We can provide invoices and receipts – just send your company details when you book.",
      },
      {
        question: "Do you operate at night and on weekends?",
        answer:
          "Yes. This route is available 24/7 with advance booking, and the price is the same day and night.",
      },
    ],

    image: "/larnaca-airport.jpg",
    bookHref: "/booking?route=nicosia-larnaca-airport",
    bookCtaLabel: "Reserve Your Taxi from Nicosia to Larnaca Airport",
    bookCtaSupport:
      "Book your fixed-price transfer and arrive at LCA relaxed and on time for your flight.",
  },

  // 2) Nicosia → Limassol
  {
    slug: "nicosia-limassol",
    from: "Nicosia",
    to: "Limassol",

    metaTitle: "Taxi from Nicosia to Limassol | Private Coastal City Transfer",
    metaDescription:
      "Private taxi from Nicosia to Limassol at a fixed price: €75 for up to 4 passengers or €100 for up to 6. No meter, no hidden extras, 24/7 service. Door-to-door transfers to Limassol Marina, seafront hotels and city areas with Wi-Fi and bottled water.",

    heroTitle: "Taxi Transfer from Nicosia to Limassol",
    subheadline:
      "Fixed Prices: €75 (up to 4 passengers) · €100 (up to 6 passengers)\nDistance: ~85–95 km · Average Journey: 1h 10–1h 25",

    body: `Connect the capital with Cyprus’s main coastal business city via our Nicosia to Limassol private taxi transfer. For €75 per car (up to 4 passengers) or €100 per minivan (up to 6 passengers), we take you directly from any address in Nicosia to Limassol Marina, the seafront, business districts or residential areas.

Whether you’re travelling for work, a cruise, a weekend break or a relocation, this door-to-door service saves you time and effort compared to buses, car rentals or self-driving. There is no meter, no per-kilometre charging and no hidden extras under normal conditions, and the price is the same day and night.

All vehicles are modern, air-conditioned and equipped with free Wi-Fi and bottled water, so you can work, rest or simply enjoy the ride.`,

    distance: "85–95 km",
    time: "1h 10–1h 25",
    sedanPrice: "€75",
    vanPrice: "€100",

    whatsIncluded: [
      "€75 per standard car (up to 4 passengers)",
      "€100 per minivan (up to 6 passengers)",
      "Pickup from any address in Nicosia (home, hotel, office, embassy, university)",
      "Drop-off at any address in Limassol (Marina, seafront, business area, suburbs)",
      "Free Wi-Fi & bottled water on board",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Business travellers, couples, small families",
        fixedPrice: "€75",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, small groups, extra luggage",
        fixedPrice: "€100",
      },
    ],

    destinationHighlights: [
      "Limassol Marina and Old Port",
      "Seafront promenade and beach hotels",
      "Business and financial districts",
      "Restaurants, shops and nightlife along the coast and in the Old Town",
    ],

    idealFor: [
      "Business travellers going between Nicosia and Limassol",
      "Families or couples changing base from the capital to the coast",
      "Cruise passengers heading to Limassol Marina",
      "Expats and residents commuting regularly between the two cities",
    ],

    faq: [
      {
        question: "Is the price per person?",
        answer:
          "No, the price is per vehicle. €75 for a standard car (up to 4 passengers) and €100 for a minivan (up to 6 passengers).",
      },
      {
        question: "Is the return Limassol → Nicosia the same price?",
        answer:
          "Yes. Normally the fare is €75 each way for a car (1–4 passengers) and €100 each way for a minivan (up to 6 passengers), unless otherwise specified in your tariff.",
      },
      {
        question: "Do you operate 24/7?",
        answer:
          "Yes, this route is available 24/7 with advance booking, and the fare is the same day and night.",
      },
      {
        question: "Can you drop me at a specific hotel, office or the Marina?",
        answer:
          "Of course. We provide door-to-door service to any Limassol address, including Limassol Marina, Old Port, seafront hotels and business districts.",
      },
    ],

    image: "/limassol.jpg",
    bookHref: "/booking?route=nicosia-limassol",
    bookCtaLabel: "Reserve Your Taxi from Nicosia to Limassol",
    bookCtaSupport:
      "Book your fixed-price transfer and enjoy a smooth, direct ride from the capital to Cyprus’s main coastal city.",
  },

  // 3) Nicosia → Paphos Airport (PFO)
  {
    slug: "nicosia-paphos-airport",
    from: "Nicosia",
    to: "Paphos Airport (PFO)",

    metaTitle:
      "Taxi from Nicosia to Paphos Airport (PFO) | Fixed-Price Airport Transfer",
    metaDescription:
      "Private taxi from Nicosia to Paphos Airport (PFO) at a fixed price: €135 for up to 4 passengers or €190 for up to 6. No hidden extras, same price day & night. Flight-safe scheduling with Wi-Fi and bottled water included.",

    heroTitle: "Taxi Transfer from Nicosia to Paphos Airport",
    subheadline:
      "Fixed Prices: €135 (up to 4 passengers) · €190 (up to 6 passengers)\nDistance: ~135–145 km · Average Journey: 1h 40–2h",

    body: `Flying out of Paphos Airport (PFO) but staying in Nicosia? Our private taxi transfer connects the capital with Paphos Airport at a clear, fixed price, taking the stress out of your long-distance departure.

For €135 per car (up to 4 passengers) or €190 per minivan (up to 6 passengers), your driver will collect you from any address in Nicosia and drive you directly to the departures area of Paphos Airport. There is no per-kilometre charging and no hidden extras under normal conditions, and the fare is the same day and night.

We plan pickup times to ensure you reach PFO with plenty of time for check-in, security and boarding, based on your airline and time of day. You can simply get in, relax, and focus on your trip.`,

    distance: "135–145 km",
    time: "1h 40–2h",
    sedanPrice: "€135",
    vanPrice: "€190",

    whatMakesBetter: [
      "Fixed prices: €135 (1–4 passengers) · €190 (up to 6 passengers)",
      "No hidden extras – same price 24/7",
      "Drivers used to airport check-in time requirements",
      "Door-to-door service from Nicosia address to Paphos Airport terminal",
      "Ideal for early-morning and late-night flights",
    ],

    whatsIncluded: [
      "€135 per standard car (up to 4 passengers)",
      "€190 per minivan (up to 6 passengers)",
      "Pickup from any Nicosia address (home, hotel, office, embassy, university)",
      "Drop-off at Paphos Airport (PFO) departures",
      "Free Wi-Fi, bottled water and air-conditioning in every vehicle",
      "Child / baby seats on request (no extra fee)",
      "Licensed, insured, English-speaking driver",
      "All tolls, VAT and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, business travellers",
        fixedPrice: "€135",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, small groups, extra luggage",
        fixedPrice: "€190",
      },
    ],

    destinationHighlights: [
      "Paphos Airport serves the Paphos region and Coral Bay.",
      "Many charter and low-cost flights to and from Europe.",
      "The long distance from Nicosia makes a direct, private transfer the easiest option.",
    ],

    idealFor: [
      "Residents of Nicosia flying from Paphos Airport (PFO)",
      "Tourists who stay in Nicosia but depart from Paphos",
      "Business travellers with flights in or out of PFO",
      "Families and groups with luggage who prefer a direct, private ride",
    ],

    faq: [
      {
        question: "How early will you pick us up?",
        answer:
          "Typically 3+ hours before departure, depending on the time of day, season and airline guidelines. We’ll suggest a pickup time that leaves a comfortable buffer for check-in and security.",
      },
      {
        question: "Is there any night surcharge?",
        answer:
          "No. The price is fixed day and night with pre-booking – no night or weekend surcharge.",
      },
      {
        question: "Is the price per car or per passenger?",
        answer:
          "The price is per vehicle. €135 for a standard car (up to 4 passengers) and €190 for a minivan (up to 6 passengers).",
      },
      {
        question: "Do you offer child seats?",
        answer:
          "Yes. Child and baby seats are available free of charge. Just tell us the age and weight of your child when booking.",
      },
    ],

    image: "/paphos-airport.jpg",
    bookHref: "/booking?route=nicosia-paphos-airport",
    bookCtaLabel: "Book Your Taxi from Nicosia to Paphos Airport",
    bookCtaSupport:
      "Book your fixed-price transfer and travel from Nicosia to PFO in comfort, with timing planned around your flight.",
  },

  // 4) Nicosia → Ercan Airport (ECN)
  {
    slug: "nicosia-ercan-airport",
    from: "Nicosia",
    to: "Ercan Airport (ECN)",

    metaTitle:
      "Taxi from Nicosia to Ercan Airport | Fast Cross-Border Transfer",
    metaDescription:
      "Private taxi from Nicosia to Ercan Airport (ECN) at a fixed price: €80 for up to 4 passengers or €110 for up to 6. No hidden extras. Short journey with experienced cross-border drivers and assistance at the Green Line checkpoint.",

    heroTitle: "Taxi Transfer from Nicosia to Ercan Airport",
    subheadline:
      "Fixed Prices: €80 (up to 4 passengers) · €110 (up to 6 passengers)\nDistance: ~23–25 km · Average Journey: 20–25 minutes (plus border time)",

    body: `Flying out of Ercan Airport (ECN) in North Cyprus and staying in Nicosia? Our Nicosia to Ercan Airport private taxi is the most convenient and comfortable way to get there, with a short drive and a clear, fixed price.

For a fixed fare of €80 per car (up to 4 passengers) or €110 per minivan (up to 6 passengers), we pick you up from any address in Nicosia (south side), drive to the most suitable checkpoint, support you through the crossing procedures and continue directly to Ercan Airport departures.

Our drivers are experienced on cross-border routes and can help you plan enough time for the journey, including potential waiting at the Green Line.`,

    distance: "23–25 km",
    time: "20–25 min + border procedure",
    sedanPrice: "€80",
    vanPrice: "€110",

    whatMakesBetter: [
      "Fixed prices: €80 (1–4 passengers) · €110 (up to 6 passengers)",
      "No hidden extras – fixed fare under normal conditions",
      "Very short driving distance – ideal for quick airport access",
      "Drivers familiar with checkpoints and Ercan Airport layout",
      "Door-to-door service from your Nicosia address to airport departures",
      "Free Wi-Fi and bottled water on board",
    ],

    whatsIncluded: [
      "€80 per standard car (up to 4 passengers)",
      "€110 per minivan (up to 6 passengers)",
      "Pickup from any Nicosia address (south side)",
      "Transfer via checkpoint to Ercan Airport departures",
      "Guidance on timing and border procedure",
      "Air-conditioned vehicle with Wi-Fi and bottled water",
      "Licensed, insured, English-speaking driver",
      "All local taxes and normal road tolls included",
      "Fixed price for normal border waiting time",
      "All prices are per vehicle, not per person.",
      "You must carry valid travel documents (ID or passport) and comply with all entry/exit rules.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Solo travellers, couples, small groups",
        fixedPrice: "€80",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, small groups, extra luggage",
        fixedPrice: "€110",
      },
    ],

    destinationHighlights: [
      "Ercan Airport (ECN) is the main airport for Northern Cyprus, used by many travellers connecting via Turkey.",
      "A pre-arranged taxi from Nicosia ensures your connection is organised, legal and on time.",
    ],

    idealFor: [
      "Travellers flying via Ercan Airport after staying in Nicosia",
      "Residents who regularly commute through ECN",
      "Business travellers needing a reliable cross-border link",
      "Guests who prefer a private, pre-booked service instead of arranging transport at the last minute",
    ],

    faq: [
      {
        question: "Is €80 per car or per passenger?",
        answer:
          "€80 is per car, for up to 4 passengers. For up to 6 passengers, the fixed minivan price is €110, also per vehicle.",
      },
      {
        question: "How much time should I allow before my flight?",
        answer:
          "We generally recommend at least 2.5–3 hours before departure to account for road time, border checks and airport procedures. Your driver can advise on the best pickup time based on your flight.",
      },
      {
        question: "Can you operate this route 24/7?",
        answer:
          "Yes, we operate this route 24/7 with advance booking, subject to checkpoint operating conditions and security rules.",
      },
      {
        question: "Is this transfer legal and safe?",
        answer:
          "Yes. We follow all legal requirements, use professional, licensed drivers and respect regulations at the Green Line checkpoints.",
      },
      {
        question: "Will the driver help with the border procedure?",
        answer:
          "Your driver will guide you as far as regulations allow, explain where to go and wait for you while you complete formalities, then continue to Ercan Airport once you have crossed.",
      },
    ],

    image: "/ercan-airport.jpg",
    bookHref: "/booking?route=nicosia-ercan-airport",
    bookCtaLabel: "Reserve Your Taxi from Nicosia to Ercan Airport",
    bookCtaSupport:
      "Book in advance to secure your pickup time, fixed price and a driver experienced with the Nicosia–Ercan route.",
  },

  // 5) Paphos Airport → Nicosia
  {
    slug: "paphos-airport-nicosia",
    from: "Paphos Airport (PFO)",
    to: "Nicosia",

    metaTitle:
      "Taxi from Paphos Airport to Nicosia | Private Transfer at a Fixed Price",
    metaDescription:
      "Book your private taxi from Paphos Airport to Nicosia at a fixed price: €135 for up to 4 passengers or €190 for up to 6. No hidden extras. 24/7 service, flight tracking, meet-and-greet, premium cars, Wi-Fi and local drivers.",

    heroTitle: "Taxi Transfer from Paphos Airport to Nicosia",
    subheadline:
      "Fixed Prices: €135 (up to 4 passengers) · €190 (up to 6 passengers)\nDistance: ~145 km · Average Journey: 1h 50–2h",

    body: `Travel from Paphos Airport to Nicosia in comfort and peace of mind with First Class Transfers. Whether you’re heading to a hotel in the city centre, the Old Town, the business district or a university campus, we provide a safe, punctual and fully private transfer with a clear, fixed price.

For €135 per car (up to 4 passengers) or €190 per minivan (up to 6 passengers), your driver will meet you inside the arrivals hall with a name sign, assist with your luggage and drive you directly to your address in Nicosia – no taxi queues, no haggling and no surprises on thWe actively monitor your flight, so your pickup is guaranteed even if your schedule changes. You’ll enjoy a clean, air-conditioned vehicle with free Wi-Fi, bottled water and phone charging available on board. Baby and child seats are available at no extra charge – ideal for families and longer journeys across the island.`,

    distance: "~145 km",
    time: "1h 50–2h",
    sedanPrice: "€135",
    vanPrice: "€190",

    whatMakesBetter: [
      "Fixed prices: €135 (1–4 passengers) · €190 (up to 6 passengers)",
      "No hidden extras – same fare day & night",
      "Professional, bilingual (EN/GR) local drivers",
      "Smooth door-to-door service directly to your hotel, office or home",
      "Ideal for business travellers, students, embassy staff and conference guests",
      "Option to pre-book your return transfer at a discounted package rate",
    ],

    whatsIncluded: [
      "€135 per standard car (up to 4 passengers)",
      "€190 per minivan (up to 6 passengers)",
      "Meet & greet at Paphos Airport (PFO) arrivals with a name sign",
      "Flight monitoring & guaranteed pickup for normal delays",
      "Free bottled water, Wi-Fi and air-conditioning in every vehicle",
      "Baby/child seats on request (no extra fee)",
      "Licensed, insured, English-speaking driver",
      "All tolls, VAT and insurance included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Business travellers, couples, small families",
        fixedPrice: "€135",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, student groups, embassy staff",
        fixedPrice: "€190",
      },
    ],

    destinationHighlights: [
      "Nicosia is the political, financial and cultural capital of Cyprus.",
      "A charming Old Town and Ledra Street.",
      "Government ministries, banks and embassies.",
      "Universities, museums, cafés, restaurants and cultural venues.",
    ],

    idealFor: [
      "Business travellers heading to offices, banks, ministries and embassies",
      "Students and visiting professors coming to Nicosia universities",
      "Tourists exploring the Old Town, museums and shopping streets",
      "Conference and event participants arriving via Paphos Airport",
    ],

    faq: [
      {
        question: "Is €135 per person or per vehicle?",
        answer:
          "The €135 fixed fare is per car, for up to 4 passengers. For up to 6 passengers, the fixed minivan price is €190, also per vehicle.",
      },
    ],

    image: "/nicosia.jpg",
    bookHref: "/booking?route=paphos-airport-nicosia",
    bookCtaLabel: "Reserve Your Taxi from Paphos Airport to Nicosia",
    bookCtaSupport:
      "Book your fixed-price transfer and arrive in the capital rested and ready for your meetings or city break.",
  },

  // 6) Paphos Airport → Limassol
  {
    slug: "paphos-airport-limassol",
    from: "Paphos Airport (PFO)",
    to: "Limassol",

    metaTitle:
      "Taxi from Paphos Airport to Limassol | Fast, Fixed-Price Transfers",
    metaDescription:
      "Fixed-price taxi from Paphos Airport to Limassol: €70 for up to 4 passengers or €95 for up to 6. 24/7 service, English-speaking drivers, meet-and-greet at arrivals, Wi-Fi and bottled water included.",

    heroTitle: "Taxi Transfer from Paphos Airport to Limassol",
    subheadline:
      "Fixed Prices: €70 (up to 4 passengers) · €95 (up to 6 passengers)\nDistance: ~60 km · Average Journey: 45–55 minutes",

    body: `Heading to Limassol from Paphos Airport? First Class Transfers offers a quick, reliable and comfortable door-to-door service from PFO to any address in Limassol.

For a fixed fare of €70 per car (up to 4 passengers) or €95 per minivan (up to 6 passengers), your driver will be waiting in the arrivals hall with a name sign and will take you directly to your hotel, apartment, cruise terminal or office in Limassol.

You skip bus connections, waiting times and meter uncertainty. All our vehicles are modern, air-conditioned and kept spotless. You’ll have free Wi-Fi, bottled water and a professional driver who knows both the coastal roads and city shortcuts, helping you arrive on time and without stress.

There is no meter, no per-kilometre charge and no hidden extras under normal conditions, and the fare is the same day and night.`,

    distance: "~60 km",
    time: "45–55 min",
    sedanPrice: "€70",
    vanPrice: "€95",

    whatsIncluded: [
      "€70 per standard car (up to 4 passengers)",
      "€95 per minivan (up to 6 passengers)",
      "Meet & greet at Paphos Airport (PFO) arrivals",
      "Door-to-door drop-off anywhere in Limassol (Marina, seafront, centre, suburbs)",
      "Free Wi-Fi and bottled water on board",
      "Baby / child seats on request (no extra fee)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, business travellers",
        fixedPrice: "€70",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, cruise groups, extra luggage",
        fixedPrice: "€95",
      },
    ],

    destinationHighlights: [
      "Limassol Marina and Old Port",
      "Seafront promenade, beaches and resorts",
      "City of Dreams Mediterranean and major conference venues",
      "Restaurants, shops, nightlife and coastal bars",
    ],

    idealFor: [
      "Cruise passengers embarking or disembarking at Limassol Marina or Old Port",
      "Business travellers attending meetings, conferences or expos",
      "Tourists staying along the Limassol seafront",
      "Families heading to resorts, waterparks and beachfront hotels",
    ],

    faq: [
      {
        question: "Is the price the same at night or on weekends?",
        answer:
          "Yes. Our €70 (car) and €95 (minivan) fares are fixed 24/7 with advance booking.",
      },
      {
        question:
          "Can you take us directly to Limassol Marina or the cruise terminal?",
        answer:
          "Absolutely. Just enter “Limassol Marina” or your ship name when booking, and your driver will take you straight there.",
      },
      {
        question: "Can I book last-minute?",
        answer:
          "Same-day bookings are often possible subject to availability, but we recommend booking in advance, especially during high season.",
      },
      {
        question: "Is the price per person or per car?",
        answer:
          "The price is per vehicle – not per person. €70 for a standard car (up to 4 passengers) and €95 for a minivan (up to 6 passengers).",
      },
      {
        question: "Do you offer child seats?",
        answer:
          "Yes, baby and child seats are available free of charge. Please tell us the age of your child when booking.",
      },
    ],

    image: "/limassol.jpg",
    bookHref: "/booking?route=paphos-airport-limassol",
    bookCtaLabel: "Book Your Taxi from Paphos Airport to Limassol",
    bookCtaSupport:
      "Reserve your fixed-price transfer and enjoy a fast, comfortable ride straight into Limassol.",
  },

  // 7) Paphos Airport → Larnaca (city)
  {
    slug: "paphos-airport-larnaca",
    from: "Paphos Airport (PFO)",
    to: "Larnaca",

    metaTitle:
      "Taxi from Paphos Airport to Larnaca | Comfortable Private Transfers",
    metaDescription:
      "Private taxi from Paphos Airport to Larnaca at a fixed price: €135 for up to 4 passengers or €175 for up to 6. No meter, no hidden extras. 24/7 service with professional drivers, Wi-Fi and door-to-door transfers.",

    heroTitle: "Taxi Transfer from Paphos Airport to Larnaca",
    subheadline:
      "Fixed Prices: €135 (up to 4 passengers) · €175 (up to 6 passengers)\nDistance: ~125 km · Average Journey: 1h 30–1h 45",

    body: `Travelling from Paphos Airport (PFO) to Larnaca? Our private taxi transfers make the cross-island trip simple, comfortable and stress-free.

For a fixed fare of €135 per car (up to 4 passengers) or €175 per minivan (up to 6 passengers), your driver will collect you from the arrivals hall and drive you directly to your hotel, seafront apartment or business address in Larnaca.

There are no taxi queues, no surge pricing and no meter surprises. Your transfer includes free Wi-Fi, bottled water, air-conditioning and generous luggage space – ideal for families, long stays and digital nomads carrying equipment.`,

    distance: "~125 km",
    time: "1h 30–1h 45",
    sedanPrice: "€135",
    vanPrice: "€175",

    whatsIncluded: [
      "€135 per standard car (up to 4 passengers)",
      "€175 per minivan (up to 6 passengers)",
      "Meet & greet at Paphos Airport arrivals with a name sign",
      "Door-to-door transfer to any Larnaca address (city, promenade, suburbs)",
      "Free Wi-Fi & bottled water in every vehicle",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "All road tolls, VAT and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, business travellers",
        fixedPrice: "€135",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, small groups, extra luggage",
        fixedPrice: "€175",
      },
    ],

    destinationHighlights: [
      "Finikoudes Promenade and seafront cafés",
      "Mackenzie Beach with bars and restaurants",
      "Local tavernas, coffee shops and neighbourhoods",
      "A convenient base for exploring the rest of Cyprus",
    ],

    idealFor: [
      "Holidaymakers staying in Larnaca city or beachfront areas",
      "Digital nomads and long-stay guests with luggage and equipment",
      "Families with children, buggies and multiple suitcases",
      "Business travellers heading straight from PFO to meetings in Larnaca",
    ],

    faq: [
      {
        question:
          "Is this service different from Paphos Airport → Larnaca Airport?",
        answer:
          "Yes. This page is for transfers to Larnaca city and coastal areas. We also offer a direct Paphos Airport → Larnaca Airport (LCA) service – please see the related route page for that transfer.",
      },
      {
        question: "Do you offer round-trip discounts?",
        answer:
          "Yes. If you book both directions in advance (for example, Larnaca → Paphos Airport on your return), we can offer package pricing. Please contact us for details.",
      },
      {
        question: "Is the price per person or per car?",
        answer:
          "The price is per vehicle. €135 for a standard car (up to 4 passengers) and €175 for a minivan (up to 6 passengers).",
      },
      {
        question: "Do you charge more at night?",
        answer:
          "No. With advance booking, the fare is the same day and night, including weekends.",
      },
      {
        question: "Can we add a supermarket stop on the way?",
        answer:
          "Yes, a short stop such as a supermarket visit can usually be added on request, subject to reasonable time.",
      },
    ],

    image: "/larnaca.jpg",
    bookHref: "/booking?route=paphos-airport-larnaca",
    bookCtaLabel: "Book Your Taxi from Paphos Airport to Larnaca",
    bookCtaSupport:
      "Reserve your fixed-price transfer and enjoy a smooth cross-island journey from Paphos Airport to Larnaca.",
  },

  // 8) Paphos Airport → Ayia Napa
  {
    slug: "paphos-airport-ayia-napa",
    from: "Paphos Airport (PFO)",
    to: "Ayia Napa",

    metaTitle:
      "Taxi from Paphos Airport to Ayia Napa | Long-Distance Premium Transfer",
    metaDescription:
      "Private taxi from Paphos Airport to Ayia Napa at a fixed price: €170 for up to 4 passengers or €200 for up to 6. No hidden extras. Long-distance comfort with Wi-Fi, child seats and experienced local drivers.",

    heroTitle: "Taxi Transfer from Paphos Airport to Ayia Napa",
    subheadline:
      "Fixed Prices: €170 (up to 4 passengers) · €200 (up to 6 passengers)\nDistance: ~170 km · Average Journey: 2h 15–2h 30",

    body: `Ayia Napa is on the opposite side of the island from Paphos – and the best way to make this long journey is in a comfortable, private taxi with a clear, fixed price.

Our Paphos Airport to Ayia Napa transfer is designed for travellers who value comfort and reliability over multiple bus changes and long waits. For €170 per car (up to 4 passengers) or €200 per minivan (up to 6 passengers), your driver will pick you up directly from Paphos Airport and take you to any hotel, villa or apartment in Ayia Napa, including Nissi Beach, the harbour area and all main resorts.

There is no per-kilometre charging and no hidden extras under normal conditions – and the price is the same day and night. You can simply sit back, enjoy the ride across Cyprus and arrive rested.`,

    distance: "~170 km",
    time: "2h 15–2h 30",
    sedanPrice: "€170",
    vanPrice: "€200",

    whatMakesBetter: [
      "Fixed prices: €170 (1–4 passengers) · €200 (up to 6 passengers)",
      "No hidden extras – fixed fare for a long-distance trip",
      "Modern, comfortable vehicles suitable for 2+ hours of driving",
      "Free Wi-Fi, bottled water and air-conditioning in every vehicle",
      "Child seats included on request for families",
      "Local drivers who know the best routes and rest stops",
      "Flight monitoring and flexible pickup time based on your arrival",
    ],

    whatsIncluded: [
      "€170 per standard car (up to 4 passengers)",
      "€200 per minivan (up to 6 passengers)",
      "Meet & greet at Paphos Airport (PFO) with a name sign",
      "Door-to-door service to any Ayia Napa hotel, villa or apartment",
      "Flight monitoring – we adjust if your landing time changes",
      "Free Wi-Fi, bottled water and air-conditioning",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "All taxes, road tolls and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, friends",
        fixedPrice: "€170",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, wedding groups, extra luggage",
        fixedPrice: "€200",
      },
    ],

    destinationHighlights: [
      "Blue Flag beaches, including Nissi Beach",
      "Nightlife, bars and beach clubs",
      "Family resorts and waterparks",
      "Harbour area, coastal walks and boat trips",
    ],

    idealFor: [
      "Families with children, buggies and luggage",
      "Couples on honeymoon or romantic breaks",
      "Groups travelling to weddings, events or parties in Ayia Napa",
      "Guests who prefer a comfortable, direct transfer instead of public transport and multiple changes",
    ],

    faq: [
      {
        question: "Are there breaks during the journey?",
        answer:
          "Yes. Your driver can stop for a short rest, coffee or toilet break on request, which is especially useful for families or longer rides.",
      },
      {
        question: "Is €170 per person?",
        answer:
          "No. €170 is for the entire car, up to 4 passengers. For up to 6 passengers, the fixed minivan price is €200 per vehicle.",
      },
      {
        question: "Do you charge extra at night or on weekends?",
        answer:
          "No. With pre-booking, the price is the same day and night, including weekends.",
      },
      {
        question: "Will you wait if my flight is delayed?",
        answer:
          "Yes. We monitor your flight and adjust the pickup time for normal delays. If there are major schedule changes, we’ll coordinate a new pickup time with you.",
      },
    ],

    image: "/ayia-napa.webp",
    bookHref: "/booking?route=paphos-airport-ayia-napa",
    bookCtaLabel: "Reserve Your Taxi from Paphos Airport to Ayia Napa",
    bookCtaSupport:
      "Secure your fixed-price cross-island transfer and arrive in Ayia Napa relaxed and ready to enjoy your stay.",
  },

  // 9) Paphos Airport → Ercan Airport (ECN)
  {
    slug: "paphos-airport-ercan-airport",
    from: "Paphos Airport (PFO)",
    to: "Ercan Airport (ECN)",

    metaTitle:
      "Taxi from Paphos Airport to Ercan Airport | Cross-Border Private Transfer",
    metaDescription:
      "Private taxi from Paphos Airport (PFO) to Ercan Airport (ECN) at a fixed price: €190 for up to 4 passengers or €230 for up to 6. No hidden extras under normal conditions. Cross-border transfer with licensed drivers, assistance at the Green Line crossing and comfortable vehicles.",

    heroTitle: "Taxi Transfer from Paphos Airport to Ercan Airport",
    subheadline:
      "Fixed Prices: €190 (up to 4 passengers) · €230 (up to 6 passengers)\nDistance: ~165–175 km · Average Journey: 2h 10–2h 30 (plus border time)",

    body: `If you’re landing at Paphos Airport (PFO) and flying out of Ercan Airport (ECN) in North Cyprus, you need a reliable, well-organised cross-border transfer. Our service connects the two airports with a private vehicle, licensed driver and clear guidance at the Green Line crossing.

For €190 per car (up to 4 passengers) or €230 per minivan (up to 6 passengers), you get a dedicated vehicle, airport-to-airport service and support during the land border procedures. There is no per-kilometre charging and no hidden extras under normal conditions.

Because this route involves a long drive and a border crossing, we strongly recommend allowing generous connection time between your arrival and departure flights.`,

    distance: "165–175 km",
    time: "2h 10–2h 30 + border procedures",
    sedanPrice: "€190",
    vanPrice: "€230",

    whatMakesBetter: [
      "Fixed cross-border prices: €190 (1–4 passengers) · €230 (up to 6 passengers)",
      "No hidden extras – fixed fare for normal border waiting time",
      "Drivers experienced with Green Line crossings and airport-to-airport routes",
      "Assistance with planning timing, so you don’t miss your onward flight",
      "Comfortable vehicles with Wi-Fi and bottled water for a 2+ hour journey",
    ],

    whatsIncluded: [
      "€190 per standard car (up to 4 passengers)",
      "€230 per minivan (up to 6 passengers)",
      "Pickup at Paphos Airport (PFO) arrivals",
      "Drop-off at Ercan Airport (ECN) departures",
      "Support and guidance at crossing points (where regulations allow)",
      "Air-conditioned vehicle with free Wi-Fi and bottled water",
      "Licensed, insured, English-speaking driver",
      "All local taxes, road tolls and normal border waiting time included",
      "All prices are per vehicle, not per person.",
      "Important: You must carry valid travel documents (ID or passport) and comply with all entry/exit rules.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Solo travellers, couples, small groups",
        fixedPrice: "€190",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, small groups, extra luggage",
        fixedPrice: "€230",
      },
    ],

    destinationHighlights: [
      "Ercan Airport (ECN) is the main airport for Northern Cyprus, used by many travellers connecting via Turkey.",
    ],

    idealFor: [
      "Travellers connecting via Paphos → Ercan on the same day",
      "Residents and expats who regularly use ECN flights via Turkey",
      "Business travellers needing a reliable, legally compliant cross-border transfer",
      "Guests who prefer a single, organised transfer instead of arranging taxis on both sides of the Green Line",
    ],

    faq: [
      {
        question: "Is €190 per person or per car?",
        answer:
          "€190 is per car, for up to 4 passengers. For up to 6 passengers, the fixed minivan price is €230, also per vehicle.",
      },
      {
        question:
          "How much connection time do I need between PFO arrival and ECN departure?",
        answer:
          "We generally recommend at least 4–5 hours between your scheduled landing at Paphos and your departure from Ercan, to cover road time, border checks and airport procedures. Your driver can advise a suitable pickup time based on your flight details.",
      },
      {
        question: "Is this transfer legal and safe?",
        answer:
          "Yes. We follow all legal requirements, use professional licensed drivers and respect regulations at the Green Line checkpoints.",
      },
      {
        question: "Will the driver help with the border procedure?",
        answer:
          "Yes – within what regulations allow. Your driver will guide you to the correct area, explain what to expect and wait for you while you complete formalities.",
      },
      {
        question: "Do you operate this route 24/7?",
        answer:
          "Yes, with advance booking and subject to checkpoint operating conditions and security rules.",
      },
    ],

    image: "/ercan-airport.jpg",
    bookHref: "/booking?route=paphos-airport-ercan-airport",
    bookCtaLabel: "Reserve Your Paphos → Ercan Airport Transfer",
    bookCtaSupport:
      "Book in advance to secure your fixed-price, cross-border transfer and a driver experienced with the Paphos–Ercan route.",
  },

  // 10) Larnaca Airport → Famagusta (North Cyprus)
  {
    slug: "larnaca-airport-famagusta",
    from: "Larnaca Airport (LCA)",
    to: "Famagusta (North Cyprus)",

    metaTitle:
      "Taxi from Larnaca Airport to Famagusta | Cross-Border Transfers at Fixed Price",
    metaDescription:
      "Private taxi from Larnaca Airport to Famagusta (North Cyprus) at a fixed price: €90 for up to 4 passengers or €110 for up to 6. Legal cross-border transfer with experienced drivers, checkpoint assistance, Wi-Fi and bottled water included.",

    heroTitle: "Taxi Transfer from Larnaca Airport to Famagusta (North Cyprus)",
    subheadline:
      "Fixed Prices: €90 (up to 4 passengers) · €110 (up to 6 passengers)\nDistance: ~60–70 km · Average Journey: 60–80 minutes (incl. border)",

    body: `Famagusta (Mağusa) in Northern Cyprus is known for its historic city walls, sandy beaches and seafront resorts. Our fixed-price Larnaca Airport to Famagusta taxi provides a safe, legal and comfortable cross-border transfer from the moment you land.

For €90 per car (up to 4 passengers) or €110 per minivan (up to 6 passengers), your driver will meet you at Larnaca Airport (LCA) arrivals with a name sign, help with your luggage, guide you through the checkpoint procedures and drive you directly to your hotel or address in Famagusta.

There is no per-kilometre charging and no hidden extras under normal conditions, and the price is the same day and night. You travel in a modern, air-conditioned vehicle with Wi-Fi and bottled water, with a professional driver who knows both the route and the border process.`,

    distance: "60–70 km",
    time: "60–80 minutes (incl. border)",
    sedanPrice: "€90",
    vanPrice: "€110",

    whatMakesBetter: [
      "Fixed cross-border prices: €90 (1–4 passengers) · €110 (up to 6 passengers)",
      "Legal, professional cross-border taxi service",
      "Drivers familiar with checkpoints and Famagusta hotels & resorts",
      "Assistance and guidance during checkpoint procedures (where regulations allow)",
      "Modern, air-conditioned vehicles with Wi-Fi and bottled water",
      "Safe, discreet service for families, couples and individual travellers",
    ],

    whatsIncluded: [
      "€90 per standard car (up to 4 passengers)",
      "€110 per minivan (up to 6 passengers)",
      "Meet & greet at Larnaca Airport arrivals",
      "Cross-border transfer via checkpoint with driver support and instructions",
      "Wi-Fi, bottled water and air-conditioning in every vehicle",
      "Licensed, insured, English-speaking driver",
      "All local taxes, road tolls and normal border waiting time included",
      "All prices are per vehicle, not per person.",
      "Reminder: A valid ID/passport is required for crossing and border waiting time may vary depending on traffic and time of day.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, solo travellers, small families",
        fixedPrice: "€90",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, small groups, extra luggage",
        fixedPrice: "€110",
      },
    ],

    destinationHighlights: [
      "Historic walled city and medieval old town streets",
      "Beachfront hotels and resorts along the coast",
      "Casino & spa properties popular with adults and groups",
      "Easy access to sandy beaches and local attractions in the region",
    ],

    idealFor: [
      "Couples staying at seafront resorts in the Famagusta area",
      "Families visiting Famagusta and surrounding beaches",
      "Guests who prefer a pre-arranged, safe cross-border ride",
      "Travellers who want a direct connection from their flight to their hotel",
    ],

    faq: [
      {
        question: "Is the price fixed even with border delays?",
        answer:
          "The fare includes standard border waiting time. If there are very long, unusual delays, your driver will inform you in advance about any potential extra waiting time charge.",
      },
      {
        question: "Do you operate this route 24/7?",
        answer:
          "Yes, we operate 24/7, subject to checkpoint operating conditions and with advance booking.",
      },
      {
        question: "Can I book a return transfer?",
        answer:
          "Yes. We can arrange your return from Famagusta to Larnaca Airport. Booking both directions in advance helps with planning and availability.",
      },
      {
        question: "Is this transfer legal and safe?",
        answer:
          "Yes. We follow all legal requirements, respect regulations at the Green Line and use licensed, professional drivers.",
      },
    ],

    image: "/famagusta.jpg",
    bookHref: "/booking?route=larnaca-airport-famagusta",
    bookCtaLabel: "Reserve Your Taxi to Famagusta",
    bookCtaSupport:
      "Book your fixed-price, legal cross-border transfer from Larnaca Airport to Famagusta and travel with peace of mind.",
  },

  // 11) Larnaca Airport → Kyrenia (Girne)
  {
    slug: "larnaca-airport-kyrenia",
    from: "Larnaca Airport (LCA)",
    to: "Kyrenia (Girne)",

    metaTitle:
      "Taxi from Larnaca Airport to Kyrenia | Secure Cross-Border Transfers",
    metaDescription:
      "Private taxi from Larnaca Airport to Kyrenia (Girne) at a fixed price: €120 for up to 4 passengers or €160 for up to 6. Legal cross-border transfer with licensed drivers, assistance at checkpoints, Wi-Fi and bottled water included.",

    heroTitle: "Taxi Transfer from Larnaca Airport to Kyrenia (Girne)",
    subheadline:
      "Fixed Prices: €120 (up to 4 passengers) · €160 (up to 6 passengers)\nDistance: ~85–95 km · Average Journey: 80–100 minutes (incl. border)",

    body: `Kyrenia (Girne) in Northern Cyprus is a popular destination for holidays, casino resorts and seafront hotels. Our fixed-price cross-border transfer from Larnaca Airport to Kyrenia provides a safe, legal and comfortable way to reach your hotel after your flight.

For €120 per car (up to 4 passengers) or €160 per minivan (up to 6 passengers), your driver will meet you at Larnaca Airport (LCA) arrivals with a name sign, assist with your luggage and drive you to Kyrenia via the appropriate checkpoint.

Crossing between the Republic of Cyprus and Northern Cyprus requires passing through a border point. Our drivers are experienced with these procedures and will guide you through each step, helping you plan enough time for both the drive and possible border queues.

There is no per-kilometre charge and no hidden extras under normal conditions, and prices are the same day and night.`,

    distance: "85–95 km",
    time: "80–100 minutes (incl. border)",
    sedanPrice: "€120",
    vanPrice: "€160",

    whatMakesBetter: [
      "Legal, professional cross-border taxi service",
      "Fixed prices: €120 (1–4 passengers) · €160 (up to 6 passengers)",
      "Fixed fare includes standard border waiting time – no surprises",
      "Drivers familiar with checkpoints and Kyrenia hotels & casinos",
      "Safe and discreet transfers for families, couples and individuals",
      "Modern vehicles with air-conditioning, Wi-Fi and bottled water",
    ],

    whatsIncluded: [
      "€120 per standard car (up to 4 passengers)",
      "€160 per minivan (up to 6 passengers)",
      "Meet & greet at Larnaca Airport arrivals",
      "Transfer via checkpoint with assistance and guidance (where regulations allow)",
      "Wi-Fi, bottled water and air-conditioning in every vehicle",
      "Licensed, insured, English-speaking driver",
      "All local taxes, road tolls and normal border waiting time included",
      "All prices are per vehicle, not per person.",
      "Important: You must carry a valid passport or ID suitable for crossing – please check entry rules in advance.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, solo travellers, small families",
        fixedPrice: "€120",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, casino groups, more luggage",
        fixedPrice: "€160",
      },
    ],

    destinationHighlights: [
      "Historic harbour and castle",
      "Casino & spa hotels along the coast",
      "Seafront promenades with harbour views",
      "Resorts suitable for couples, families and groups",
    ],

    idealFor: [
      "Tourists staying in Kyrenia hotels & casinos",
      "Families visiting relatives in Northern Cyprus",
      "Guests wanting a safe, organised cross-border transfer",
      "Travellers who prefer one continuous journey instead of changing taxis at the checkpoint",
    ],

    faq: [
      {
        question: "Do I need a passport?",
        answer:
          "Yes. You must carry a valid ID/passport suitable for crossing between the Republic of Cyprus and Northern Cyprus. Always check the latest entry/exit rules before travelling.",
      },
      {
        question: "Is the price fixed even if the border is busy?",
        answer:
          "The price includes standard border waiting time. If there is an exceptionally long delay, the driver will clearly explain any extra waiting charge before continuing.",
      },
      {
        question: "Is this transfer legal and safe?",
        answer:
          "Yes. We follow all legal requirements, respect regulations at checkpoints and use licensed, professional drivers.",
      },
      {
        question: "Can you bring us back from Kyrenia to Larnaca Airport?",
        answer:
          "Yes. We also offer Kyrenia → Larnaca Airport transfers. You can pre-book a return for peace of mind and better planning.",
      },
    ],

    image: "/kyrenia.jpg",
    bookHref: "/booking?route=larnaca-airport-kyrenia",
    bookCtaLabel: "Reserve Your Taxi to Kyrenia",
    bookCtaSupport:
      "Book your fixed-price, legal cross-border transfer from Larnaca Airport to Kyrenia and travel with peace of mind.",
  },

  // 12) Larnaca Airport → Limassol
  {
    slug: "larnaca-airport-limassol",
    from: "Larnaca Airport (LCA)",
    to: "Limassol",

    metaTitle:
      "Taxi from Larnaca Airport to Limassol | Fixed-Price City & Marina Transfers",
    metaDescription:
      "Book your private taxi from Larnaca Airport to Limassol for a fixed price: €70 for up to 4 passengers or €95 for up to 6. 24/7 service, modern vehicles, meet-and-greet at arrivals. Ideal for Limassol Marina, seafront hotels and business trips.",

    heroTitle: "Taxi Transfer from Larnaca Airport to Limassol",
    subheadline:
      "Fixed Prices: €70 (up to 4 passengers) · €95 (up to 6 passengers)\nDistance: ~67–72 km · Average Journey: 50–60 minutes",

    body: `Heading to Limassol for business, a cruise or a beach holiday? Our fixed-price taxi from Larnaca Airport to Limassol gives you a comfortable, reliable and stress-free start to your trip.

Your driver will meet you inside the arrivals hall with a name sign, assist with your luggage and drive you directly to your hotel, apartment, Limassol Marina or the Old Port. There’s no need to queue for a taxi or worry about the final fare.

All vehicles are modern, fully air-conditioned and equipped with free Wi-Fi and bottled water. You can choose between a standard car (up to 4 passengers) or a spacious minivan (up to 6 passengers) – perfect for families, groups and corporate travellers.`,

    distance: "67–72 km",
    time: "50–60 minutes",
    sedanPrice: "€70",
    vanPrice: "€95",

    whatMakesBetter: [
      "Fixed prices: €70 (1–4 passengers) · €95 (up to 6 passengers)",
      "24/7 availability with advance booking",
      "No hidden extras – same price day and night",
      "Drivers experienced with Limassol Marina, seafront hotels and business districts",
      "Ideal for cruise passengers and conference visitors",
      "Direct motorway route – no unnecessary stops or detours",
      "Option to book return transfers or additional city-to-city legs",
    ],

    whatsIncluded: [
      "€70 per standard car (up to 4 passengers)",
      "€95 per minivan (up to 6 passengers)",
      "Airport meet & greet service at Larnaca arrivals",
      "Free Wi-Fi & bottled water in every vehicle",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls and parking included",
      "Private, door-to-door service – no sharing with other passengers",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, business travellers",
        fixedPrice: "€70",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, groups, extra luggage",
        fixedPrice: "€95",
      },
    ],

    destinationHighlights: [
      "Limassol Marina & Old Port – yachts, cruises, restaurants and bars",
      "Seafront promenade and city beaches",
      "Luxury resorts in the Amathus and Agios Tychonas areas",
      "Corporate offices, financial district and conference venues",
    ],

    idealFor: [
      "Cruise and marina passengers",
      "Business travellers and conference guests",
      "Couples and families staying at seafront resorts",
      "Groups of up to 6 with extra luggage or equipment",
    ],

    faq: [
      {
        question: "Is €70 a fixed price?",
        answer:
          "Yes. €70 is the fixed fare for a standard car (1–4 passengers) on this route. There are no night, weekend or luggage surcharges.",
      },
      {
        question: "We are 5 or 6 passengers – how much is the transfer?",
        answer:
          "For groups of up to 6 passengers, we offer a minivan at a fixed price of €95 for this route. You can select the minivan option in the booking form.",
      },
      {
        question: "Do you cover Limassol Marina and Old Port hotels?",
        answer:
          "Yes. The same route fare applies to Limassol Marina, Old Port and main seafront hotels in the Limassol urban area.",
      },
      {
        question: "Do you operate at night or early in the morning?",
        answer:
          "Yes. This route is available 24/7 with advance booking. The price is the same day and night.",
      },
    ],

    image: "/limassol.jpg",
    bookHref: "/booking?route=larnaca-airport-limassol",
    bookCtaLabel: "Reserve Your Taxi to Limassol",
    bookCtaSupport:
      "Secure your fixed price today and have your driver waiting at Larnaca Airport when you land.",
  },

  // 13) Larnaca Airport → Nicosia
  {
    slug: "larnaca-airport-nicosia",
    from: "Larnaca Airport (LCA)",
    to: "Nicosia",

    metaTitle:
      "Taxi from Larnaca Airport to Nicosia | Executive-Style Fixed-Price Transfer",
    metaDescription:
      "Private taxi from Larnaca Airport to Nicosia at a fixed price: €55 for up to 4 passengers or €80 for up to 6. No hidden extras, same price day & night. Ideal for business travellers, embassies, students and city breaks.",

    heroTitle: "Taxi Transfer from Larnaca Airport to Nicosia",
    subheadline:
      "Fixed Prices: €55 (up to 4 passengers) · €80 (up to 6 passengers)\nDistance: ~52–60 km · Average Journey: 40–50 minutes",

    body: `Travel from Larnaca Airport to Nicosia – the capital of Cyprus – with a professional, executive-style transfer. Perfect for business travellers, embassy staff, students and tourists staying in the historic centre or modern districts like Engomi and Strovolos.

For a fixed price of €55 per car (up to 4 passengers) or €80 per minivan (up to 6 passengers), you get a fare that does not change with traffic, time of day or normal flight delays. There is nd no hidden extras – what you see when you book is what you pay.

Your driver will wait inside arrivals with a name sign, assist with your luggage and drive you directly to your hotel, office, university or residence in Nicosia.

All vehicles offer air-conditioning, Wi-Fi and bottled water, and child seats are available free of charge.`,

    distance: "52–60 km",
    time: "40–50 minutes",
    sedanPrice: "€55",
    vanPrice: "€80",

    whatMakesBetter: [
      "Executive-style service for business & embassy travellers",
      "Fixed €55 (1–4 passengers) · €80 (up to 6 passengers)",
      "No hidden extras – same price day and night",
      "Drivers familiar with ministries, embassies and universities",
      "Invoices and receipts available for corporate clients",
      "24/7 availability for early or late flights",
    ],

    whatsIncluded: [
      "€55 per standard car (up to 4 passengers)",
      "€80 per minivan (up to 6 passengers)",
      "Meet & greet at Larnaca Airport arrivals",
      "Wi-Fi, bottled water and air-conditioning in every vehicle",
      "Child / baby seats on request (free of charge)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls & parking included",
      "Fixed price 24/7 – no night or weekend surcharges",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Business travellers, solo travellers, small teams",
        fixedPrice: "€55",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, embassy groups, extra luggage",
        fixedPrice: "€80",
      },
    ],

    destinationHighlights: [
      "Government ministries and embassies",
      "Historic walled city and Ledra Street",
      "Universities and corporate offices",
      "Restaurants, cafés and cultural venues",
    ],

    idealFor: [
      "Business travellers and corporate clients",
      "Embassy staff and official visitors",
      "Students and academic staff",
      "Tourists staying in the capital",
    ],

    faq: [
      {
        question: "Is €55 per person or per car?",
        answer:
          "€55 is per car, for up to 4 passengers. For up to 6 passengers, the fixed minivan price is €80, also per vehicle.",
      },
      {
        question: "Do you use  add extras later?",
        answer:
          "No. All our transfers are on a fixed-price basis – nd no hidden extras. Your confirmed price already includes VAT, tolls and standard waiting time.",
      },
      {
        question: "Do you charge extra at night or on weekends?",
        answer:
          "No. The price is the same 24/7, regardless of day, night or weekend, as long as the transfer is booked in advance.",
      },
      {
        question: "Do you cover Engomi, Strovolos and embassy areas?",
        answer:
          "Yes. All central Nicosia districts, including Engomi, Strovolos, City Centre and embassy areas, are covered at the same fare.",
      },
    ],

    image: "/nicosia.jpg",
    bookHref: "/booking?route=larnaca-airport-nicosia",
    bookCtaLabel: "Reserve Your Taxi to Nicosia",
    bookCtaSupport:
      "Secure your fixed, all-inclusive price and have your driver waiting at Larnaca Airport when you land.",
  },

  // 14) Larnaca Airport → Paphos
  {
    slug: "larnaca-airport-paphos",
    from: "Larnaca Airport (LCA)",
    to: "Paphos",

    metaTitle:
      "Taxi from Larnaca Airport to Paphos | Comfortable Long-Distance Transfers",
    metaDescription:
      "Private taxi from Larnaca Airport to Paphos at a fixed price: €130 for up to 4 passengers or €175 for up to 6. No hidden extras, same price day & night. 24/7 service, comfort stops, Wi-Fi and bottled water. Ideal for Kato Paphos and seafront resorts.",

    heroTitle: "Taxi Transfer from Larnaca Airport to Paphos",
    subheadline:
      "Fixed Prices: €130 (up to 4 passengers) · €175 (up to 6 passengers)\nDistance: ~130–140 km · Average Journey: 90–100 minutes",

    body: `The journey from Larnaca Airport to Paphos is one of the longest on the island. Our fixed-price private transfer ensures you travel in comfort, without worrying about thraffic or hidden surcharges.

For €130 per car (up to 4 passengers) or €175 per minivan (up to 6 passengers), your price is fully fixed – day and night. There is nd no extra per kilometre charges. What you book is exactly what you pay.

Your driver will greet you at arrivals with a name sign, help with luggage and drive you along the highway directly to your hotel or apartment in Paphos, Kato Paphos or nearby resort areas. Short comfort or coffee stops can be arranged on the way if needed, especially for families with children or older travellers.`,

    distance: "130–140 km",
    time: "90–100 minutes",
    sedanPrice: "€130",
    vanPrice: "€175",

    whatMakesBetter: [
      "Long-distance specialists with comfortable, well-maintained vehicles",
      "Fixed prices: €130 (1–4 passengers) · €175 (up to 6 passengers)",
      "No hidden extras – same price day and night",
      "Ideal for families, couples and older travellers",
      "Optional rest / coffee stop during the journey",
      "Drivers familiar with major hotels, resorts and Kato Paphos seafront",
    ],

    whatsIncluded: [
      "€130 per standard car (up to 4 passengers)",
      "€175 per minivan (up to 6 passengers)",
      "Meet & greet at Larnaca Airport arrivals",
      "Free Wi-Fi, bottled water & air-conditioning in every vehicle",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls & parking included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, business travellers",
        fixedPrice: "€130",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, groups, extra luggage",
        fixedPrice: "€175",
      },
    ],

    destinationHighlights: [
      "Archaeological sites, mosaics and the harbour promenade",
      "Resorts in Kato Paphos and nearby Coral Bay",
      "Family hotels and adults-only spa resorts",
      "Beautiful sunsets, coastal walks and relaxed nightlife",
    ],

    idealFor: [
      "Families with children and luggage",
      "Couples on longer stays in the Paphos region",
      "Older travellers who prefer a direct, door-to-door service",
      "Guests who want a private, comfortable transfer instead of shared shuttles",
    ],

    faq: [
      {
        question: "Is €130 per car or per person?",
        answer:
          "€130 is per car, for up to 4 passengers. For up to 6 passengers, the fixed minivan price is €175, also per vehicle.",
      },
      {
        question: "Do you use  charge extra per kilometre?",
        answer:
          "No. This is a fixed-price transfer – nd no extra per kilometre charges. Your confirmed price already includes VAT, tolls and standard waiting time.",
      },
      {
        question: "Do you charge extra at night or on weekends?",
        answer:
          "No. The price is the same 24/7, including night arrivals and weekend flights, as long as you book in advance.",
      },
      {
        question: "Can we have a rest stop on the way?",
        answer:
          "Yes. Short rest or coffee stops can be arranged on request, which is especially helpful for families with children or older passengers.",
      },
    ],

    image: "/paphos.jpg",
    bookHref: "/booking?route=larnaca-airport-paphos",
    bookCtaLabel: "Reserve Your Taxi to Paphos",
    bookCtaSupport:
      "Secure your fixed, all-inclusive price and enjoy a smooth, private transfer from Larnaca Airport to Paphos.",
  },

  // 15) Limassol → Ercan Airport (ECN)
  {
    slug: "limassol-ercan-airport",
    from: "Limassol",
    to: "Ercan Airport (ECN)",

    metaTitle:
      "Taxi from Limassol to Ercan Airport | Cross-Border Private Transfer",
    metaDescription:
      "Private taxi from Limassol to Ercan Airport (ECN) at a fixed price: €130 for up to 4 passengers or €170 for up to 6. Experienced cross-border drivers, Wi-Fi on board, assistance at Green Line checkpoints. Advance booking recommended.",

    heroTitle: "Taxi Transfer from Limassol to Ercan Airport",
    subheadline:
      "Fixed Prices: €130 (up to 4 passengers) · €170 (up to 6 passengers)\nDistance: ~110–125 km · Average Journey: 1h 45–2h 10 (including border crossing)",

    body: `Need to travel from Limassol to Ercan Airport (ECN) in North Cyprus? Our cross-border taxi service offers a safe, comfortable and legal way to reach your flight with fixed, pre-agreed prices and experienced drivers who regularly cross the Green Line.

For €130 per car (up to 4 passengers) or €170 per minivan (up to 6 passengers), you travel with no per-kilometre charges and no hidden extras under normal conditions. Your driver will pick you up anywhere in Limassol, drive to the appropriate checkpoint, guide you through the border procedure and continue to Ercan Airport departures.

Because this route involves a border crossing, we strongly recommend allowing extra time for formalities, especially during busy periods.`,

    distance: "110–125 km",
    time: "1h 45–2h 10 + border checks",
    sedanPrice: "€130",
    vanPrice: "€170",

    whatMakesBetter: [
      "Fixed cross-border prices: €130 (1–4 passengers) · €170 (up to 6 passengers)",
      "No hidden extras – fixed fare including normal border waiting time",
      "Drivers experienced with Green Line crossings and procedures",
      "Assistance and guidance at the checkpoint",
      "Comfortable vehicles suitable for a ~2-hour journey",
      "24/7 service with advance booking",
    ],

    whatsIncluded: [
      "€130 per standard car (up to 4 passengers)",
      "€170 per minivan (up to 6 passengers)",
      "Pickup anywhere in Limassol (hotel, apartment, office)",
      "Drop-off at Ercan Airport (ECN) departures",
      "Free Wi-Fi & bottled water on board",
      "Air-conditioning and comfortable seating",
      "Licensed, insured, English-speaking driver",
      "VAT, road tolls and normal border waiting time included",
      "All prices are per vehicle, not per person.",
      "Important: A valid passport or ID is required for Green Line crossings. Border waiting times can vary; in the case of exceptional, extended delays, any extra waiting charge will be discussed with you in advance.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Solo travellers, couples, small groups",
        fixedPrice: "€130",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, small groups, extra luggage",
        fixedPrice: "€170",
      },
    ],

    destinationHighlights: [
      "Direct cross-border link from Limassol to Ercan Airport",
      "Suitable for onward connections via Turkey",
    ],

    idealFor: [
      "Travellers flying from Ercan Airport after staying in Limassol",
      "Residents and expats with connections via ECN",
      "Passengers who prefer a private, organised cross-border transfer rather than arranging taxis on both sides of the Green Line",
    ],

    faq: [
      {
        question: "Is the fare affected by border delays?",
        answer:
          "The fixed price includes normal waiting time at the checkpoint. In the event of exceptional or very long delays, the driver will clearly explain any potential extra waiting charge before proceeding, so there are no surprises.",
      },
      {
        question: "Do you operate 24/7?",
        answer:
          "Yes, but we strongly recommend advance booking and allowing extra time for your transfer, especially for early-morning or late-night flights.",
      },
      {
        question: "Is the price per person or per vehicle?",
        answer:
          "The price is per vehicle. €130 for a standard car (up to 4 passengers) and €170 for a minivan (up to 6 passengers).",
      },
      {
        question: "Do I need a passport or ID to cross?",
        answer:
          "Yes. A valid passport or ID is required for Green Line crossings. Please make sure your travel documents are valid before booking.",
      },
      {
        question: "Will the driver help me at the border?",
        answer:
          "Yes. Your driver will guide you through the process as far as regulations allow, explain where to go and wait for you on the other side of the checkpoint.",
      },
    ],

    image: "/ercan-airport.jpg",
    bookHref: "/booking?route=limassol-ercan-airport",
    bookCtaLabel: "Reserve Your Taxi from Limassol to Ercan Airport",
    bookCtaSupport:
      "Book in advance to secure your pickup time, fixed price and a driver experienced with the Limassol–Ercan route.",
  },

  // 16) Limassol → Nicosia
  {
    slug: "limassol-nicosia",
    from: "Limassol",
    to: "Nicosia",

    metaTitle: "Taxi from Limassol to Nicosia | Capital City Private Transfer",
    metaDescription:
      "Private taxi from Limassol to Nicosia at a fixed price: €75 for up to 4 passengers or €100 for up to 6. No hidden extras, same price day and night. 24/7 availability, ideal for business, embassies, universities and city breaks.",

    heroTitle: "Taxi Transfer from Limassol to Nicosia",
    subheadline:
      "Fixed Prices: €75 (up to 4 passengers) · €100 (up to 6 passengers)\nDistance: ~85–95 km · Average Journey: 1h 10–1h 25",

    body: `Whether you’re travelling for business, studies or a city visit, our Limassol to Nicosia taxi transfer makes the journey between Cyprus’s two main cities fast, comfortable and predictable.

For a fixed price of €75 per car (up to 4 passengers) or €100 per minivan (up to 6 passengers), we pick you up at any address in Limassol and take you directly to any address in Nicosia. There is no per-kilometre charging and no hidden extras under normal conditions.

No timetables, no bus changes, no dragging luggage – just a direct city-to-city ride in a modern, air-conditioned vehicle with Wi-Fi and bottled water on board.`,

    distance: "85–95 km",
    time: "1h 10–1h 25",
    sedanPrice: "€75",
    vanPrice: "€100",

    whatMakesBetter: [
      "Fixed prices: €75 (1–4 passengers) · €100 (up to 6 passengers)",
      "No hidden extras – same price day & night",
      "Door-to-door service between Limassol and the capital",
      "Drivers familiar with embassies, ministries, universities and business areas",
      "Perfect for meetings, conferences, official visits and city breaks",
    ],

    whatsIncluded: [
      "€75 per standard car (up to 4 passengers)",
      "€100 per minivan (up to 6 passengers)",
      "Pickup at any Limassol hotel, apartment or office",
      "Drop-off at any Nicosia address (Old Town, Engomi, Strovolos, etc.)",
      "Free Wi-Fi & bottled water in every vehicle",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Solo travellers, couples, small teams",
        fixedPrice: "€75",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, small groups, extra luggage",
        fixedPrice: "€100",
      },
    ],

    destinationHighlights: [
      "Government ministries and foreign embassies",
      "The historic Old Town and Ledra Street",
      "Universities and major corporate offices",
      "Cafés, restaurants and cultural attractions",
    ],

    idealFor: [
      "Business and government travellers",
      "Embassy staff, consultants and corporate visitors",
      "Students and academics commuting between Limassol and Nicosia",
      "Tourists visiting the capital for a day trip or overnight stay",
    ],

    faq: [
      {
        question: "Is the fare per person?",
        answer:
          "No. The fare is per vehicle. €75 for a standard car (up to 4 passengers) and €100 for a minivan (up to 6 passengers).",
      },
      {
        question: "Do you use  add extras later?",
        answer:
          "No. This is a fixed-price transfer – nd no hidden extras under normal traffic conditions. Your confirmed price already includes VAT and tolls.",
      },
      {
        question: "Do you offer late-night or early-morning trips?",
        answer:
          "Yes. This route is available 24/7 with pre-booking, and the price is the same day and night.",
      },
      {
        question: "Can I get an invoice for my company?",
        answer:
          "Yes. We can provide receipts and invoices – just send your company details when you book.",
      },
    ],

    image: "/nicosia.jpg",
    bookHref: "/booking?route=limassol-nicosia",
    bookCtaLabel: "Book Your Taxi from Limassol to Nicosia",
    bookCtaSupport:
      "Reserve your fixed-price transfer and enjoy a smooth, direct ride between Limassol and Nicosia.",
  },

  // 17) Limassol → Paphos Airport (PFO)
  {
    slug: "limassol-paphos-airport",
    from: "Limassol",
    to: "Paphos Airport (PFO)",

    metaTitle:
      "Taxi from Limassol to Paphos Airport (PFO) | Fixed-Price Airport Transfer",
    metaDescription:
      "Private taxi from Limassol to Paphos Airport (PFO) at a fixed price: €70 for up to 4 passengers or €95 for up to 6. No hidden extras, no night surcharge. 24/7 service, door-to-door pickup, perfect for departures and arrivals.",

    heroTitle: "Taxi Transfer from Limassol to Paphos Airport",
    subheadline:
      "Fixed Prices: €70 (up to 4 passengers) · €95 (up to 6 passengers)\nDistance: ~60–65 km · Average Journey: 45–55 minutes",

    body: `Flying from Paphos Airport (PFO) but staying in Limassol? Our private taxi from Limassol to Paphos Airport is the easiest way to reach your flight on time – without parking stress, rental car returns orprises.

For a fixed price of €70 per car (up to 4 passengers) or €95 per minivan (up to 6 passengers), your driver will pick you up from any address in Limassol and drive you directly to the departures terminal at Paphos Airport. There is no per-kilometre charge and no hidden extras under normal conditions.

You just choose your pickup time, meet your driver at the door and enjoy a smooth, direct ride to the airport.`,

    distance: "60–65 km",
    time: "45–55 minutes",
    sedanPrice: "€70",
    vanPrice: "€95",

    whatMakesBetter: [
      "Fixed prices: €70 (1–4 passengers) · €95 (up to 6 passengers)",
      "No hidden extras – no night surcharge",
      "Pickup from hotel, marina, apartment or office in Limassol",
      "Route planned to ensure on-time arrival for check-in",
      "Ideal for both tourists and residents flying from Paphos Airport",
    ],

    whatsIncluded: [
      "€70 per standard car (up to 4 passengers)",
      "€95 per minivan (up to 6 passengers)",
      "Door-to-door pickup anywhere in Limassol",
      "Drop-off at Paphos Airport (PFO) departures",
      "Free Wi-Fi and bottled water in every vehicle",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls and normal waiting time included",
      "Fixed price 24/7 – same fare day and night",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Solo travellers, couples, small families",
        fixedPrice: "€70",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, small groups, extra bags",
        fixedPrice: "€95",
      },
    ],

    destinationHighlights: [
      "Paphos Airport serves Paphos, Kato Paphos and west-coast resorts such as Coral Bay.",
    ],

    idealFor: [
      "Guests who holiday in Limassol but fly from Paphos",
      "Residents commuting to PFO for work travel",
      "Families and groups who prefer a private, direct transfer instead of intercity buses or shared shuttles",
    ],

    faq: [
      {
        question: "How early will you collect us?",
        answer:
          "Typically 2.5–3 hours before departure, depending on the season, time of day and airline requirements. We’ll advise a suitable pickup time when you book.",
      },
      {
        question: "Do you offer child seats?",
        answer:
          "Yes. Child and baby seats are available free of charge – just tell us the age of your child when booking.",
      },
      {
        question: "Is the fare per person or per car?",
        answer:
          "The fare is per vehicle. €70 for a standard car (up to 4 passengers) and €95 for a minivan (up to 6 passengers).",
      },
      {
        question: "Do you charge extra at night or early in the morning?",
        answer:
          "No. This route is available 24/7 with pre-booking, and the price is the same day and night.",
      },
    ],

    image: "/paphos-airport.jpg",
    bookHref: "/booking?route=limassol-paphos-airport",
    bookCtaLabel: "Book Your Taxi from Limassol to Paphos Airport",
    bookCtaSupport:
      "Reserve your fixed-price transfer and arrive at PFO on time, without parking or rental car hassle.",
  },

  // 18) Limassol → Paphos (city)
  {
    slug: "limassol-paphos",
    from: "Limassol",
    to: "Paphos",

    metaTitle: "Taxi from Limassol to Paphos | Coastal City Transfer",
    metaDescription:
      "Private taxi from Limassol to Paphos at a fixed price: €85 for up to 4 passengers or €100 for up to 6. No hidden extras, 24/7 service. Door-to-door transfers to Paphos and Kato Paphos seafront hotels with Wi-Fi and bottled water included.",

    heroTitle: "Taxi Transfer from Limassol to Paphos",
    subheadline:
      "Fixed Prices: €85 (up to 4 passengers) · €100 (up to 6 passengers)\nDistance: ~65–70 km · Average Journey: 50–60 minutes",

    body: `Heading west along the coast? Our Limassol to Paphos private taxi takes you directly from your hotel or home in Limassol to any address in Paphos or Kato Paphos, with a clear, fixed price.

For €85 per car (up to 4 passengers) or €100 per minivan (up to 6 passengers), you avoid bus connections, parking and luggage hassle – just sit back and enjoy a comfortable transfer between two of Cyprus’s most popular coastal cities. There is no per-kilometre charging and no hidden extras under normal conditions, and the price is the same day and night.`,

    distance: "65–70 km",
    time: "50–60 minutes",
    sedanPrice: "€85",
    vanPrice: "€100",

    whatMakesBetter: [
      "Fixed prices: €85 (1–4 passengers) · €100 (up to 6 passengers)",
      "No hidden extras – same fare 24/7",
      "Door-to-door service from Limassol to Paphos / Kato Paphos",
      "Drivers familiar with hotels and apartments around Kato Paphos and the seafront",
      "Wi-Fi, bottled water and air-conditioning included in every vehicle",
    ],

    whatsIncluded: [
      "€85 per standard car (up to 4 passengers)",
      "€100 per minivan (up to 6 passengers)",
      "Pickup from any address in Limassol (hotel, apartment, office, marina)",
      "Drop-off at any address in Paphos or Kato Paphos",
      "Free Wi-Fi & bottled water on board",
      "Child / baby seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, business travellers",
        fixedPrice: "€85",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Larger families, small groups, extra luggage",
        fixedPrice: "€100",
      },
    ],

    destinationHighlights: [
      "Harbour area and coastal promenade",
      "Kato Paphos hotels and beach resorts",
      "Archaeological sites and family attractions",
      "Nearby Coral Bay (served via a separate route)",
    ],

    idealFor: [
      "Families and couples changing resort city",
      "Guests starting their holiday in Limassol and continuing in Paphos",
      "Visitors planning to explore both coasts during one trip",
    ],

    faq: [
      {
        question: "Do you also go to Coral Bay?",
        answer:
          "Yes – we offer a separate Limassol → Coral Bay route. Check the dedicated page or ask us for details.",
      },
      {
        question: "Is the price per car or per person?",
        answer:
          "The price is per car, not per person. €85 for a standard car (up to 4 passengers) and €100 for a minivan (up to 6 passengers).",
      },
      {
        question: "Can I book last-minute?",
        answer:
          "Last-minute bookings are possible subject to availability, but we recommend advance booking to secure your preferred time.",
      },
      {
        question: "Do you charge extra at night or early in the morning?",
        answer:
          "No. Our Limassol → Paphos transfers are available 24/7, and the fare is the same day and night with pre-booking.",
      },
    ],

    image: "/paphos.jpg",
    bookHref: "/booking?route=limassol-paphos",
    bookCtaLabel: "Reserve Your Taxi from Limassol to Paphos",
    bookCtaSupport:
      "Book your fixed-price transfer and enjoy a smooth coastal ride from Limassol to Paphos.",
  },

  // 19) Limassol → Troodos
  {
    slug: "limassol-troodos",
    from: "Limassol",
    to: "Troodos",

    metaTitle:
      "Taxi from Limassol to Troodos | Private Transfer to the Mountains",
    metaDescription:
      "Private taxi from Limassol to Troodos at a fixed price: €45 for up to 4 passengers or €95 for up to 6. No hidden extras. Scenic mountain drive with experienced drivers and door-to-door service.",

    heroTitle: "Taxi Transfer from Limassol to Troodos",
    subheadline:
      "Fixed Prices: €45 (up to 4 passengers) · €95 (up to 6 passengers)\nDistance: ~45–55 km · Average Journey: 50–70 minutes",

    body: `Looking for a cool escape from the coast? Our Limassol to Troodos taxi transfer takes you from the seafront straight into the heart of the mountains with a clear, fixed price.

For €45 per car (up to 4 passengers) or €95 per minivan (up to 6 passengers), you travel comfortably from any address in Limassol to Troodos Square or directly to your chosen hotel or guesthouse. There is no per-kilometre charging and no hidden extras under normal conditions – the price is the same day and night.

Our drivers are used to winding mountain roads and changing weather, including winter conditions. You can relax and enjoy the scenery, forests and villages along the way, without worrying about driving, parking or road familiarity.`,

    distance: "45–55 km",
    time: "50–70 minutes",
    sedanPrice: "€45",
    vanPrice: "€95",

    whatMakesBetter: [
      "Fixed prices: €45 (1–4 passengers) · €95 (up to 6 passengers)",
      "No hidden extras – same fare 24/7",
      "Drivers experienced with mountain routes and winter conditions",
      "Drop-off at Troodos Square, hotels, guesthouses or hiking starting points",
      "Option for short stops at viewpoints or villages (on request)",
    ],

    whatsIncluded: [
      "€45 per standard car (up to 4 passengers)",
      "€95 per minivan (up to 6 passengers)",
      "Pickup anywhere in Limassol (hotel, apartment, marina, office)",
      "Drop-off in Troodos village / square / chosen hotel or lodge",
      "Comfortable, air-conditioned vehicle (heating for winter rides)",
      "Free Wi-Fi and bottled water on board",
      "Local tips on hikes, villages, viewpoints and tavernas",
      "Licensed, insured, English-speaking driver",
      "VAT, tolls and normal waiting time included",
      "Fixed price 24/7 – no night or weekend surcharge",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, solo travellers",
        fixedPrice: "€45",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Hiking groups, larger families, extra luggage",
        fixedPrice: "€95",
      },
    ],

    destinationHighlights: [
      "Cool mountain air in summer, snow in winter",
      "Scenic trails, waterfalls and forest walks",
      "Nearby villages like Platres, Kakopetria and Omodos",
      "Traditional tavernas, cafés and small hotels / lodges",
    ],

    idealFor: [
      "Day trips from Limassol to the mountains",
      "Hiking groups and nature lovers",
      "Couples and families looking for a change of scenery",
      "Guests staying in Limassol who want to visit Troodos without renting a car",
    ],

    faq: [
      {
        question: "Is €45 per vehicle?",
        answer:
          "Yes. €45 is the fixed price for a standard car (up to 4 passengers). For up to 6 passengers, the fixed minivan price is €95 per vehicle.",
      },
      {
        question: "Do you operate this route in winter?",
        answer:
          "Yes. We operate this route year-round. In periods of heavy snow or difficult conditions, travel times may be longer and we will advise you accordingly.",
      },
      {
        question:
          "Can we combine Troodos with other villages, like Omodos or Kakopetria?",
        answer:
          "Yes. We can create a custom day-trip including Troodos and villages such as Omodos, Platres or Kakopetria. Tell us your plan and we’ll prepare a quote.",
      },
      {
        question: "Can we stop for photos or a short walk?",
        answer:
          "Short stops at viewpoints or villages are possible on request. If you’d like a full sightseeing itinerary, we can price it as a half-day or full-day trip.",
      },
    ],

    image: "/troodos.jpeg",
    bookHref: "/booking?route=limassol-troodos",
    bookCtaLabel: "Reserve Your Taxi from Limassol to Troodos",
    bookCtaSupport:
      "Book your fixed-price mountain transfer and enjoy a safe, scenic ride from Limassol to Troodos.",
  },

  // 20) Nicosia → Troodos
  {
    slug: "nicosia-troodos",
    from: "Nicosia",
    to: "Troodos Mountains",

    metaTitle:
      "Taxi from Nicosia to Troodos | Private Mountain Transfer (from €80)",
    metaDescription:
      "Private taxi from Nicosia to the Troodos Mountains from €80. Fixed price per vehicle, experienced mountain drivers, flexible stops and door-to-door service. Ideal for day trips, hiking and ski season.",

    heroTitle: "Taxi Transfer from Nicosia to Troodos Mountains",
    subheadline:
      "Fixed Prices: €80 (up to 4 passengers) · €110 (up to 6 passengers)\nDistance: 80–85 km · Average Journey: 1h 20–1h 40",

    body: `Escape the city and head into the fresh mountain air of Troodos with a private taxi from Nicosia. Whether you’re planning a hiking day, a cool summer escape, a winter ski trip, or a quiet village stay, our door-to-door transfer is the most comfortable and time-efficient way to travel from the capital to the Troodos Mountains.

Your driver will collect you from your home, hotel, office or university in Nicosia and drive you safely into the mountains, with optional short photo or coffee stops along the way. No need to worry about mountain roads, parking or winter conditions – you simply relax and enjoy the scenery.`,

    distance: "80–85 km",
    time: "1h 20–1h 40",
    sedanPrice: "€80",
    vanPrice: "€110",

    whatMakesBetter: [
      "Fixed price per vehicle – €80 (1–4 passengers) · €110 (up to 6 passengers)",
      "No meter, no night surcharge – same price day & night",
      "Drivers experienced with mountain roads and winter conditions",
      "Flexible drop-off at Troodos Square, hotels, lodges or trailheads",
      "Perfect for day trips, hiking weekends or ski season",
      "Comfortable sedans and V-Class minivans for groups & families",
    ],

    whatsIncluded: [
      "€80 per standard car (up to 4 passengers)",
      "€110 per minivan (up to 6 passengers)",
      "Door-to-door pickup from any address in Nicosia",
      "Drop-off at Troodos Square, hotels, lodges or trailheads",
      "Air-conditioned vehicle suitable for mountain driving",
      "Free Wi-Fi & bottled water",
      "Baby/child seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "All tolls, VAT and insurance included",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, hikers",
        fixedPrice: "€80",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, groups, ski or hiking equipment",
        fixedPrice: "€110",
      },
    ],

    destinationHighlights: [
      "Cooler temperatures in summer – perfect escape from city heat",
      "Scenic hiking trails, forests and waterfalls",
      "Ski area in winter (seasonal)",
      "Nearby traditional villages like Platres, Kakopetria and Pedoulas",
      "Stone-built guesthouses, cosy hotels and mountain tavernas",
    ],

    idealFor: [
      "Day trips from Nicosia",
      "Hikers, cyclists and nature lovers",
      "Families seeking cooler weather in summer",
      "Couples on scenic mountain getaways",
      "Groups travelling with luggage or ski equipment",
    ],

    faq: [
      {
        question: "Is €80 per person or per car?",
        answer:
          "The €80 fare is per car, for up to 4 passengers. For up to 6 passengers, the fixed price is €110 per minivan.",
      },
      {
        question: "Is there any extra charge at night or on weekends?",
        answer:
          "No. Prices are fixed 24/7 for pre-booked transfers – no night or weekend surcharge.",
      },
      {
        question: "Can we stop on the way for photos or coffee?",
        answer:
          "Yes. Short photo or comfort stops are included – just ask your driver.",
      },
      {
        question: "Do you operate in winter when there is snow?",
        answer:
          "Yes, we operate all year. Travel time may be longer during heavy snow, and your driver will advise you if needed.",
      },
      {
        question:
          "Can we combine Troodos with villages like Platres or Omodos in one trip?",
        answer:
          "Yes. We can arrange a customised day trip with multiple stops. Contact us for a tailored quote.",
      },
    ],

    image: "/troodos.jpeg",
    bookHref: "/booking?route=nicosia-troodos",
    bookCtaLabel: "Book Your Taxi from Nicosia to Troodos",
    bookCtaSupport:
      "Reserve your fixed-price mountain transfer and enjoy a comfortable, scenic ride from Nicosia to the Troodos Mountains.",
  },

  // 🔧 TEST ROUTE — FOR DEVELOPMENT ONLY
  {
    slug: "nicosia-test-destination",
    from: "Nicosia",
    to: "Test Destination",

    metaTitle:
      "Taxi from Nicosia to Test Destination | Private Mountain Transfer (from €1)",
    metaDescription:
      "Private taxi from Nicosia to the Test Destination Mountains from €1. Fixed price per vehicle, experienced mountain drivers, flexible stops and door-to-door service. Ideal for day trips, hiking and ski season.",

    heroTitle: "Taxi Transfer from Nicosia to Test Destination Mountains",
    subheadline:
      "Fixed Prices: €1 (up to 4 passengers) · €1 (up to 6 passengers)\nDistance: 80–85 km · Average Journey: 1h 20–1h 40",

    body: `Escape the city and head into the fresh mountain air of Test Destination with a private taxi from Nicosia. Whether you’re planning a hiking day, a cool summer escape, a winter ski trip, or a quiet village stay, our door-to-door transfer is the most comfortable and time-efficient way to travel from the capital to the Test Destination Mountains.

Your driver will collect you from your home, hotel, office or university in Nicosia and drive you safely into the mountains, with optional short photo or coffee stops along the way. No need to worry about mountain roads, parking or winter conditions – you simply relax and enjoy the scenery.`,

    distance: "80–85 km",
    time: "1h 20–1h 40",
    sedanPrice: "€1",
    vanPrice: "€1",

    whatMakesBetter: [
      "Fixed price per vehicle – €1 (1–4 passengers) · €1 (up to 6 passengers)",
      "No meter, no night surcharge – same price day & night",
      "Drivers experienced with mountain roads and winter conditions",
      "Flexible drop-off at Test Destination Square, hotels, lodges or trailheads",
      "Perfect for day trips, hiking weekends or ski season",
      "Comfortable sedans and V-Class minivans for groups & families",
    ],

    whatsIncluded: [
      "€1 per standard car (up to 4 passengers)",
      "€1 per minivan (up to 6 passengers)",
      "Door-to-door pickup from any address in Nicosia",
      "Drop-off at Test Destination Square, hotels, lodges or trailheads",
      "Air-conditioned vehicle suitable for mountain driving",
      "Free Wi-Fi & bottled water",
      "Baby/child seats on request (no extra charge)",
      "Licensed, insured, English-speaking driver",
      "All tolls, VAT and insurance included",
      "All prices are per vehicle, not per person.",
    ],

    vehicleOptions: [
      {
        type: "Standard Car",
        maxPassengers: "up to 4",
        idealFor: "Couples, small families, hikers",
        fixedPrice: "€1",
      },
      {
        type: "Minivan",
        maxPassengers: "up to 6",
        idealFor: "Families, groups, ski or hiking equipment",
        fixedPrice: "€1",
      },
    ],

    destinationHighlights: [
      "Cooler temperatures in summer – perfect escape from city heat",
      "Scenic hiking trails, forests and waterfalls",
      "Ski area in winter (seasonal)",
      "Nearby traditional villages like Platres, Kakopetria and Pedoulas",
      "Stone-built guesthouses, cosy hotels and mountain tavernas",
    ],

    idealFor: [
      "Day trips from Nicosia",
      "Hikers, cyclists and nature lovers",
      "Families seeking cooler weather in summer",
      "Couples on scenic mountain getaways",
      "Groups travelling with luggage or ski equipment",
    ],

    faq: [
      {
        question: "Is €1 per person or per car?",
        answer:
          "The €1 fare is per car, for up to 4 passengers. For up to 6 passengers, the fixed price is €1 per minivan.",
      },
      {
        question: "Is there any extra charge at night or on weekends?",
        answer:
          "No. Prices are fixed 24/7 for pre-booked transfers – no night or weekend surcharge.",
      },
      {
        question: "Can we stop on the way for photos or coffee?",
        answer:
          "Yes. Short photo or comfort stops are included – just ask your driver.",
      },
      {
        question: "Do you operate in winter when there is snow?",
        answer:
          "Yes, we operate all year. Travel time may be longer during heavy snow, and your driver will advise you if needed.",
      },
      {
        question:
          "Can we combine Test Destination with villages like Platres or Omodos in one trip?",
        answer:
          "Yes. We can arrange a customised day trip with multiple stops. Contact us for a tailored quote.",
      },
    ],

    image: "/protaras.jpg",
    bookHref: "/booking?route=nicosia-test-destination",
    bookCtaLabel: "Book Your Taxi from Nicosia to Test Destination",
    bookCtaSupport:
      "Reserve your fixed-price mountain transfer and enjoy a comfortable, scenic ride from Nicosia to the Troodos Mountains.",
  },
];

// helper
export function getRouteDetailBySlug(slug: string): RouteDetail | undefined {
  return ROUTE_DETAILS.find((r) => r.slug === slug);
}
