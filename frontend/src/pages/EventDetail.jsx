import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getEvents, purchaseEvent } from "../api";

export default function EventDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [event, setEvent] = useState(null);
  const [form, setForm] = useState({
    name: "",
    email: "",
    paymentMethod: "card",
    discountCode: "",
  });
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  // Fetch event details
  useEffect(() => {
    getEvents().then((events) => {
      const found = events.find((e) => e.id === Number(id));
      setEvent(found || null);
    });
  }, [id]);

  const handleChange = (e) => {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Manual validation in Spanish
    if (!form.name.trim()) {
      setError("Por favor ingresa tu nombre.");
      return;
    }
    if (!form.email.trim()) {
      setError("Por favor ingresa tu correo.");
      return;
    }
    // (Optional) Extra: check for valid email format
    if (!/\S+@\S+\.\S+/.test(form.email)) {
      setError("Por favor ingresa un correo válido.");
      return;
    }

    setStatus(null);

    try {
      const res = await purchaseEvent({
        name: form.name,
        email: form.email,
        event_id: event.id,
        payment_method: form.paymentMethod,
        discount_code: form.discountCode,
      });
      setStatus(res.status);
    } catch (err) {
      setError("Ocurrió un error al procesar la compra.");
    }
  };

  if (!event) return <div className="p-6">Cargando evento...</div>;

  // Show result if purchased
  if (status === "paid")
    return (
      <div className="p-6 text-center">
        <h2 className="text-2xl font-bold mb-2">✅ ¡Pago exitoso!</h2>
        <p>
          Te has inscrito correctamente en <b>{event.name}</b>.
        </p>
        <button
          className="mt-4 px-4 py-2 bg-[#FF6F61] rounded text-white"
          onClick={() => navigate("/store")}
        >
          Volver a la vitrina
        </button>
      </div>
    );
  if (status === "failed")
    return (
      <div className="p-6 text-center">
        <h2 className="text-2xl font-bold mb-2">❌ Pago rechazado</h2>
        <p>
          Tu pago no fue aprobado. Puedes intentar con otro método o revisar los
          datos ingresados.
        </p>
        <button
          className="mt-4 px-4 py-2 bg-[#FF6F61] rounded text-white"
          onClick={() => setStatus(null)}
        >
          Intentar nuevamente
        </button>
      </div>
    );

  return (
    <div className="max-w-md mx-auto p-6 bg-[#1A1C26] rounded-lg text-white">
      <h2 className="text-2xl font-bold mb-2">{event.name}</h2>
      <p className="mb-2">{event.description}</p>
      <p>
        <b>Precio:</b> ${event.price.toLocaleString("es-CL")}
      </p>
      <p>
        <b>Duración:</b> {event.duration}
      </p>
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Tu nombre"
          className="w-full p-2 rounded bg-[#22232d] text-white"
        />
        <input
          name="email"
          value={form.email}
          onChange={handleChange}
          placeholder="Tu correo"
          className="w-full p-2 rounded bg-[#22232d] text-white"
        />
        <div className="flex gap-4">
          <label>
            <input
              type="radio"
              name="paymentMethod"
              value="card"
              checked={form.paymentMethod === "card"}
              onChange={handleChange}
            />{" "}
            Tarjeta
          </label>
          <label>
            <input
              type="radio"
              name="paymentMethod"
              value="other"
              checked={form.paymentMethod === "other"}
              onChange={handleChange}
            />{" "}
            Otro medio
          </label>
        </div>
        <input
          name="discountCode"
          value={form.discountCode}
          onChange={handleChange}
          placeholder="Código de descuento (opcional)"
          className="w-full p-2 rounded bg-[#22232d] text-white"
        />
        <button
          className="w-full py-2 bg-[#FF6F61] rounded text-white font-bold"
          type="submit"
        >
          Pagar e Inscribirme
        </button>
        {error && <div className="text-red-400 text-sm">{error}</div>}
      </form>
    </div>
  );
}
