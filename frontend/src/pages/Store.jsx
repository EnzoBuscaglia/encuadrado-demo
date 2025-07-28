import { useEffect, useState } from "react";
import { getContents, getEvents } from "../api";

export default function Store() {
  const [events, setEvents] = useState([]);
  const [contents, setContents] = useState([]);

  useEffect(() => {
    getEvents().then(setEvents);
    getContents().then(setContents);
  }, []);

  const now = new Date();

  return (
    <div className="w-screen h-screen bg-[#1A1C26] text-white p-6 overflow-hidden">
      <div className="flex items-center justify-center mb-6 gap-3">
        <img
          src="/encuadrado2.png"
          alt="Encuadrado Logo"
          className="w-10 h-10"
        />
        <h1 className="text-4xl font-bold">La Vitrina</h1>
      </div>
      <div className="flex h-[90%]">
        {/* Events Column */}
        <section className="w-1/2 h-full overflow-y-scroll pr-2 border-r border-[#FCECEA]/20">
          <h2 className="text-2xl font-bold mb-4 text-[#FAFAFA]">📅 Eventos</h2>
          <div className="space-y-4">
            {events.map((event) => {
              const eventDate = new Date(event.start_time);
              const isPast = eventDate < now;
              const isFull = event.is_full;
              const isDisabled = isPast || isFull;

              return (
                <div
                  key={event.id}
                  className={`p-4 rounded-lg shadow bg-[#FF6F61] transition-colors ${
                    isDisabled
                      ? "opacity-50 pointer-events-none"
                      : "hover:bg-[#F05A4F]"
                  }`}
                >
                  <h3 className="text-lg font-semibold text-[#FAFAFA]">
                    {event.name}
                  </h3>
                  <p className="text-sm text-[#FCECEA]">{event.description}</p>
                  <p className="text-sm mt-2 font-medium text-[#FAFAFA]">
                    Precio: ${event.price.toLocaleString("es-CL")}
                  </p>
                  <a
                    href={`/store/event/${event.id}`}
                    className={`text-[#FCECEA] underline text-sm mt-2 block ${
                      isDisabled ? "cursor-not-allowed" : ""
                    }`}
                    tabIndex={isDisabled ? -1 : 0}
                    aria-disabled={isDisabled}
                  >
                    Ver más
                  </a>
                  {isFull && (
                    <div className="text-sm text-yellow-100 mt-1 font-semibold">
                      Sin cupos disponibles
                    </div>
                  )}
                  {isPast && (
                    <div className="text-sm text-yellow-100 mt-1 font-semibold">
                      Evento finalizado
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Digital Content Column */}
        <section className="w-1/2 h-full overflow-y-scroll pl-2">
          <h2 className="text-2xl font-bold mb-4 text-[#FAFAFA]">
            📦 Contenido Digital
          </h2>
          <div className="space-y-4">
            {contents.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-lg shadow bg-[#FF6F61] hover:bg-[#F05A4F] transition-colors"
              >
                <h3 className="text-lg font-semibold text-[#FAFAFA]">
                  {item.name}
                </h3>
                <p className="text-sm text-[#FCECEA]">{item.description}</p>
                <p className="text-sm mt-2 font-medium text-[#FAFAFA]">
                  Precio: ${item.price.toLocaleString("es-CL")}
                </p>
                <a
                  href={`/store/content/${item.id}`}
                  className="text-[#FCECEA] underline text-sm mt-2 block"
                >
                  Ver más
                </a>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
