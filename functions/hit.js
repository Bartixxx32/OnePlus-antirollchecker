export async function onRequest(context) {
  const { request } = context;

  try {
    // Wywołanie Workera pod nowym URL (oparb.bartixxx.workers.dev/hit)
    // Forwardujemy nagłówki, żeby Worker dostał IP końcowego użytkownika
    await fetch("https://oparb.bartixxx.workers.dev/hit", {
      method: request.method,
      headers: request.headers
    });

    // Zawsze zwracamy OK – żeby frontend/apka nie zauważyła zmiany
    return new Response("OK", {
      status: 200,
      headers: {
        "Content-Type": "text/plain",
        "Access-Control-Allow-Origin": "*"
      }
    });
  } catch (err) {
    return new Response("Error", { status: 500 });
  }
}
