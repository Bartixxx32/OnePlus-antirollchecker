export async function onRequest(context) {
  const { request, env } = context;
  
  if (!env.HITS_KV) {
    return new Response(JSON.stringify({ error: "KV namespace HITS_KV not bound" }), { 
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    // 1. Zliczanie ogólnych hitów
    const totalHitsKey = "total_hits";
    let totalHits = parseInt(await env.HITS_KV.get(totalHitsKey)) || 0;
    totalHits += 1;
    await env.HITS_KV.put(totalHitsKey, totalHits.toString());

    // 2. Liczenie unikalnych użytkowników dziennie
    const ip = request.headers.get("cf-connecting-ip") || "unknown";
    const today = new Date().toISOString().split("T")[0];
    const uniqueDayKey = `unique:${today}:${ip}`;
    const dailyUniqueCounterKey = `daily_unique:${today}`;

    const alreadyHit = await env.HITS_KV.get(uniqueDayKey);
    let dailyUnique = parseInt(await env.HITS_KV.get(dailyUniqueCounterKey)) || 0;

    if (!alreadyHit) {
      dailyUnique += 1;
      await env.HITS_KV.put(dailyUniqueCounterKey, dailyUnique.toString());
      // Zapisujemy hit IP na 24h
      await env.HITS_KV.put(uniqueDayKey, "1", { expirationTtl: 86400 });
    }

    return new Response(JSON.stringify({
      status: "ok",
      total_hits: totalHits,
      daily_unique: dailyUnique
    }), {
      headers: { 
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*" // Opcjonalnie dla aplikacji mobilnej/webowej
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { 
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
