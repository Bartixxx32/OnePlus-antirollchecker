export async function onRequest(context) {
  try {
    return Response.redirect("https://oparb.bartixxx.workers.dev/hit", 302);
  } catch (err) {
    return new Response("Error", { status: 500 });
  }
}