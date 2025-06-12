/**
 * Worker que recibe POST en /summarize y reenvía al modelo
 */
export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const body = await request.json();
    const { text, min_length, max_length } = body;
    if (!text || text.length < 50) {
      return new Response(
        JSON.stringify({ error: 'El texto debe tener al menos 50 caracteres.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Llamada a la API de resumen externa (puede ser HF en un endpoint o RapidAPI)
    const apiUrl = env.WORKER_URL_TARGET; // definir en wrangler.toml vars o en entorno
    const apiResponse = await fetch(apiUrl + '/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.CF_API_TOKEN}`,
      },
      body: JSON.stringify({ text, min_length, max_length }),
    });

    if (!apiResponse.ok) {
      const error = await apiResponse.text();
      return new Response(error, { status: apiResponse.status });
    }

    const data = await apiResponse.json();
    return new Response(JSON.stringify({ summary: data.summary }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: 'Error interno en el Worker' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}