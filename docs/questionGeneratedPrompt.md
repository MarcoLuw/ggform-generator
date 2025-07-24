You are a senior English teacher and assessment designer. Your task is to generate high-quality multiple-choice questions (MCQs) to help learners understand and remember English vocabulary more effectively.

## Objective:
Generate one creative, pedagogically effective MCQ per vocabulary item using the provided structured vocabulary list.

## Input Format:
The user will provide a list of vocabulary items in the following JSON format:
{
  "Vocabulary": "cement (v)",
  "Meaning": "to make something strong, fixed, or permanent",
  "Collocation": "Cement someone’s status - to firmly confirm their reputation, success, or position\n\n(Củng cố vị thế của ai đó)",
  "Context": "Her latest win cemented her status as a top athlete.\n→ The win confirmed and strengthened her reputation.\n\nThe luxury and exclusivity cements Via Monte Napoleone's status as a premier shopping destination.",
  "IPA": null,
  "Time": "05/07/2025"
}

## Requirements:
- Create one MCQ per vocabulary item.
- Use the **Vocabulary**, **Meaning**, **Collocation**, and **Context** fields to construct the question.
- Be creative: vary the question format (e.g., choose the best synonym, complete the sentence, find the best usage).
- Each question must be understandable, educational, and help reinforce meaning and usage.
- Use realistic, age-appropriate contexts. Avoid outdated, awkward, or overly complex wording.
- Include an explanation that reinforces the correct answer and references the meaning, collocation, and context provided.
- Each MCQ must have 4 options (1 correct + 3 plausible distractors).
- Avoid repeated or overly similar options.

## Output Format:
Return the MCQs as a list of JSON objects in the following format:

[
  {
    "question": "Your question here...",
    "options": {
      "option-1": "Answer A",
      "option-2": "Answer B",
      "option-3": "Answer C",
      "option-4": "Answer D"
    },
    "correct_option": "option-3",
    "explanation": "Detailed explanation supporting the correct answer, with references to the vocabulary’s meaning, collocation, or usage context."
  },
  ...
]

## Example Guidance for the AI (if helpful):
- Use clues from the **Collocation** and **Context** fields to build realistic, scenario-based questions.
- Distractors should be grammatically or semantically similar but clearly incorrect upon closer inspection.
- The tone should be friendly, educational, and suitable for upper-intermediate to advanced ESL learners.

Begin generating MCQs from the provided vocabulary list:

[
    {
        "Meaning": "To be positioned snugly or securely in a place, often surrounded or protected by something.",
        "Collocation": "nestle somewhere",
        "Context": "Bregenz is a pretty Austrian town that nestles between the Alps and Lake Constance",
        "IPA": "/ˈnes.əl/",
        "Time": "05/07/2025",
        "Vocabulary": "nestle (v)"
    },
    {
        "Meaning": "a street, often a wide one, in a city or town\n\nđại lộ",
        "Collocation": null,
        "Context": "New York avenue has become a beacon for luxury",
        "IPA": "/ˈæv.ə.nuː/",
        "Time": "05/07/2025",
        "Vocabulary": "avenue (n)"
    },
    {
        "Meaning": "to attract attention or interest",
        "Collocation": "draw someone’s attention to something",
        "Context": "The vibrant avenue draws fashion enthusiasts and high society attention from around the globe",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "draw (v)"
    },
    {
        "Meaning": null,
        "Collocation": null,
        "Context": null,
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "fashion enthusiasts"
    },
    {
        "Meaning": "rich, powerful, and fashionable people\n\ngiới thượng lưu",
        "Collocation": null,
        "Context": null,
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "high society"
    },
    {
        "Meaning": "energetic, exciting, and full of enthusiasm",
        "Collocation": null,
        "Context": "a vibrant city\na vibrant avenue\na vibrant young performer",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "vibrant (adj)"
    },
    {
        "Meaning": "go beyond, exceed, or do better than someone or something",
        "Collocation": null,
        "Context": "He hopes to surpass his rival in the next race.\n\n→ He wants to beat his competitor.",
        "IPA": "/sɚˈpæs/",
        "Time": "05/07/2025",
        "Vocabulary": "surpass"
    },
    {
        "Meaning": "something is believed to be caused by or the result of something else",
        "Collocation": "[Effect] is attributed to [Cause]",
        "Context": "His success is attributed to hard work and determination.\n→ (He wants to beat his competitor.)\n\nThis surge is attributed to the street’s limited space\n→ Mức tăng này được cho là do diện tích hạn chế của con phố",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "be attributed to"
    },
    {
        "Meaning": "limited access, special rights\n\nthe right to have or do something that is limited to only one person or organization\n\ntính độc quyền",
        "Collocation": null,
        "Context": "The company has an exclusivity agreement with that supplier.\n→ Only that company can buy from the supplier — no competitors allowed.",
        "IPA": "/ˌeks.kluːˈsɪv.ə.t̬i/",
        "Time": "05/07/2025",
        "Vocabulary": "exclusivity (n)"
    },
    {
        "Meaning": "to rise very quickly to a high level",
        "Collocation": null,
        "Context": "Gold prices have soared in 2025.\n→ Prices increased a lot and quickly.",
        "IPA": "/sɔːr/",
        "Time": "05/07/2025",
        "Vocabulary": "soar (v)"
    },
    {
        "Meaning": "to add something decorative to a person or thing",
        "Collocation": "be adorned with",
        "Context": "The bride's hair was adorned with white flowers.\n\nThe street is adorned with flagship stores of renowned luxury brands such as Fendi, Prada, Gucci, and Chanel",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "adorn (v)"
    },
    {
        "Meaning": "the biggest or most important shop that a company owns",
        "Collocation": null,
        "Context": null,
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "flagship store"
    },
    {
        "Meaning": "famous for something",
        "Collocation": null,
        "Context": "The region is renowned for its outstanding natural beauty.\n\nDucati is one of the most renowned brands in the world",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "renowned (adj)"
    },
    {
        "Meaning": "something is worth the time, effort, or money spent on it",
        "Collocation": null,
        "Context": "That movie was really worthwhile.\n→ It was a good use of time — enjoyable or meaningful.\n\nIt wasn’t easy, but the experience was worthwhile.\n→ The results or lessons made the effort worth it.\n\na worthwhile investment",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "worthwhile (adj)"
    },
    {
        "Meaning": "the quality of being attractive, interesting, or exciting",
        "Collocation": null,
        "Context": "The allure of the city lights drew him in.\n→ The city lights had an irresistible charm.\n\nThe Via Monte Napoleone avenue has its own retail allure.\n→ Đại lộ Monte có một sức hấp dẫn về bán lẻ của chính nó",
        "IPA": "/əˈlʊr/",
        "Time": "05/07/2025",
        "Vocabulary": "allure (n)"
    },
    {
        "Meaning": "to support, improve or strengthen something",
        "Collocation": null,
        "Context": "She tried to bolster my confidence/morale \n→ encourage me and make me feel stronger\n\nMilan’s vibrant fashion scene is bolstered by international fashion weeks and design events",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "bolster (v)"
    },
    {
        "Meaning": "không khí thời trang",
        "Collocation": null,
        "Context": null,
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "fashion scene (n)"
    },
    {
        "Meaning": "attract or tempt someone to do something, often by offering something appealing or desirable.\n\ndụ dỗ, thu hút",
        "Collocation": null,
        "Context": "The advertisement enticed customers with special discounts.\n→ It attracted customers by offering something appealing.",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "entice (v)"
    },
    {
        "Meaning": "lasting for a long time",
        "Collocation": "enduring appeal - something that stays popular, interesting, or loved over a long time",
        "Context": "the enduring appeal of cartoons\n\nThe film has an enduring appeal even after 30 years.\n→ People still enjoy it decades later.\n\nClassic fashion has an enduring appeal.\n→ Timeless styles remain attractive, no matter the trends.",
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "enduring (adj)"
    },
    {
        "Meaning": "attractiveness, charm, or the ability to attract interest",
        "Collocation": null,
        "Context": null,
        "IPA": null,
        "Time": "05/07/2025",
        "Vocabulary": "appeal (n)"
    }
]