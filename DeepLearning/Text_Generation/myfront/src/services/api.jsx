const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function sendQuestion(question) {
  try {
    const res = await fetch(`${BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(errorText);
    }

    return res.json(); // { answer: "...", sources: [...] }
  } catch (err) {
    console.error("Erreur fetch:", err);
    throw err;
  }
}
