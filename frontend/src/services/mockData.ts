import type {
  Series,
  Episode,
  Genre,
  Source,
  ImportJob,
  DiscoveredSeries,
  RightsRecord,
  VideoAsset,
  TakedownRequest,
  AnalyticsSummary,
} from '../types'
import catalogData from './catalog.json'

export const MOCK_GENRES: Genre[] = [
  {
    "id": "1",
    "name": "Romance",
    "slug": "romance",
    "icon": "❤️"
  },
  {
    "id": "2",
    "name": "Venganza",
    "slug": "venganza",
    "icon": "⚔️"
  },
  {
    "id": "3",
    "name": "Multimillonario",
    "slug": "multimillonario",
    "icon": "💎"
  },
  {
    "id": "4",
    "name": "Fantasía",
    "slug": "fantasia",
    "icon": "✨"
  },
  {
    "id": "5",
    "name": "Pasión",
    "slug": "pasion",
    "icon": "🔥"
  },
  {
    "id": "6",
    "name": "Mafia",
    "slug": "mafia",
    "icon": "🕶️"
  },
  {
    "id": "7",
    "name": "Suspenso",
    "slug": "suspenso",
    "icon": "⚡"
  },
  {
    "id": "8",
    "name": "Dramas Cortos",
    "slug": "dramas-cortos",
    "icon": "🎬"
  }
];

export const MOCK_SERIES: Series[] = catalogData.series as unknown as Series[];

export const MOCK_EPISODES: Record<string, Episode[]> = catalogData.episodes as unknown as Record<string, Episode[]>;

export const MOCK_SOURCES: Source[] = [
  {
    "id": "src-1",
    "name": "DramaShorts",
    "baseUrl": "https://dramashorts.io",
    "scraperType": "nextjs",
    "enabled": true,
    "totalDiscovered": 15,
    "totalImported": 15,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "src-2",
    "name": "GoodShort",
    "baseUrl": "https://www.goodshort.com",
    "scraperType": "vue_ssr",
    "enabled": true,
    "totalDiscovered": 12,
    "totalImported": 12,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "src-3",
    "name": "NetShort",
    "baseUrl": "https://netshort.com",
    "scraperType": "nextjs_app_router",
    "enabled": true,
    "totalDiscovered": 12,
    "totalImported": 12,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "src-4",
    "name": "ReelShort",
    "baseUrl": "https://www.reelshort.com",
    "scraperType": "aes_decryptor",
    "enabled": true,
    "totalDiscovered": 6,
    "totalImported": 6,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "src-5",
    "name": "StardustTV",
    "baseUrl": "https://www.stardusttv.net/es",
    "scraperType": "nuxt3_devalue",
    "enabled": true,
    "totalDiscovered": 31,
    "totalImported": 31,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "src-6",
    "name": "DramaBox",
    "baseUrl": "https://www.dramabox.com/es",
    "scraperType": "nextjs_dramabox",
    "enabled": true,
    "totalDiscovered": 42,
    "totalImported": 42,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "src-7",
    "name": "ShortTV",
    "baseUrl": "https://www.shorttv.live",
    "scraperType": "nuxt3_shorttv",
    "enabled": true,
    "totalDiscovered": 45,
    "totalImported": 45,
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-03-01T00:00:00Z"
  }
];

export const MOCK_IMPORT_JOBS: ImportJob[] = [
  {
    "id": "job-1",
    "sourceId": "src-5",
    "sourceName": "StardustTV",
    "startedAt": "2026-03-01T10:00:00Z",
    "completedAt": "2026-03-01T10:05:00Z",
    "status": "completed",
    "recordsDiscovered": 31,
    "recordsImported": 31,
    "recordsSkipped": 0,
    "recordsFailed": 0
  },
  {
    "id": "job-2",
    "sourceId": "src-7",
    "sourceName": "ShortTV",
    "startedAt": "2026-03-01T10:06:00Z",
    "completedAt": "2026-03-01T10:12:00Z",
    "status": "completed",
    "recordsDiscovered": 45,
    "recordsImported": 45,
    "recordsSkipped": 0,
    "recordsFailed": 0
  }
];

export const MOCK_DISCOVERED: DiscoveredSeries[] = [
  {
    "id": "disc-ds-1",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "mi-prometido-me-vendio-a-dos-bestias-ardientes",
    "title": "Mi prometido me vendió a dos bestias ardientes",
    "synopsis": "La noche después de su boda, Ava descubre la traición: su flamante esposo, Eliot, la empuja a una grieta sin fondo que se abre en el bosque. Despierta en un mundo oscuro y retorcido… y no fue un accidente. Eliot la “pagó” como parte de un trato con la Red Queen.\nEn la mansión la esperan Simon y Chesi: sus captores, que además la desean abiertamente. Desde las sombras observa el misterioso Hatter, atado a la Queen, intentando ocultar que a él también le importa Ava.\nPara llegar hasta la Queen, Ava deberá atravesar un bosque lleno de criaturas peligrosas, una escalera que se desmorona bajo sus pies y al Caterpillar, un tentador que le ofrece una falsa ilusión de felicidad. Al final, la Queen le da a Ava una elección: quedarse en ese mundo para siempre… o matar a Eliot y recuperar su libertad.",
    "posterUrl": "/cdn-proxy/img/movies/Q3QbdSiJR83zUZ-OHRuaCDI4/cover-es.png?v=1791210291518",
    "episodeCount": 13,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-2",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "mi-ex-me-hizo-engordar-dulce-venganza",
    "title": "¡Mi ex me hizo engordar! Dulce venganza",
    "synopsis": "Crystal, 20, cree que su novio está a punto de pedirle matrimonio. Pero diez bloggers irrumpen en el restaurante y, en un directo, descubre que él es el bromista más famoso del país… y que todo su año juntos fue un plan para engordarla y sacar contenido. Arruinada, humillada y viral, Ryan —un camarero que resulta ser el dueño del local— la ayuda a levantarse y odia a su ex tanto como ella. Un año después, Crystal está delgada, rica y es copropietaria de un imperio de restaurantes. En secreto financia el concurso de bloggers que su ex espera ganar. Él no la reconoce: se enamora de ella. Y solo Crystal sabe que la prometida de Ryan se ha estado acostando con su ex todo este tiempo.",
    "posterUrl": "/cdn-proxy/img/movies/9isHmu9iqaLjOd66VTnzPqc9/cover-es.png?v=1791201779917",
    "episodeCount": 10,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-3",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "cada-noche-llevaba-el-rostro-de-su-hermana",
    "title": "Cada noche llevaba el rostro de su hermana",
    "synopsis": "Con su padre incriminado y en la cárcel, y su madrastra y hermanastros huyendo con todo lo que pudieron cargar, Mira Kessler acepta un trato que nadie más se atreve a tomar: casarse con Audrey Ashford, la heredera de la familia más rica de Chicago, marcada por cicatrices y postrada en cama, y darle un hijo. A cambio, los Ashford liberarán a su padre.\n\nCada noche, su nueva esposa acude a su cama en absoluta oscuridad, envuelta en vendas, con una voz rota. Cada día, Jude, la fría e insoportable hermana de Audrey, le advierte que huya. Cuanto más se acerca Mira a su esposa en la oscuridad, más se siente atraída por la hermana a la luz.\n\nLo que Mira no sabe es que son la misma mujer. Audrey no puede tener hijos, los Ashford nunca pensaron liberar a su padre y la licencia matrimonial que firmó sin leer lleva el nombre de otra persona.",
    "posterUrl": "/cdn-proxy/img/movies/nBHx_2wgDiLGvhDANB2EQ2pk/cover-es.png?v=1791540283983",
    "episodeCount": 26,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-4",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "mi-padre-me-aposto-al-haren-del-capo",
    "title": "Mi padre me apostó al harén del capo",
    "synopsis": "Su padre, adicto al juego, lo apuesta en una última mano de póker. En una sola noche, Leonardo lo pierde todo: a su padre lo acribillan y Hugo, el jefe de la mafia, lo reclama para su harén. Herido y perseguido, huye por el alféizar de una ventana y termina en el apartamento de Niko, el sicario más peligroso de la ciudad. Leonardo solo le pide una cosa: enséñame a matar. Niko le da un mes. Pero el entrenamiento se convierte en una atracción imposible de negar… hasta que Leonardo encuentra un contrato con su propia cara. ¿El hombre que le enseña a sobrevivir es quien fue contratado para entregarlo? ¿Puede el amor sobrevivir en un mundo donde todos tienen un precio?",
    "posterUrl": "/cdn-proxy/img/movies/NIT9SacvrO_wkCANkINbYQvO/cover-es.png?v=1791469401785",
    "episodeCount": 13,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-5",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "me-converti-en-sirena-para-espiar-al-principe-sireno",
    "title": "Me convertí en sirena para espiar al Príncipe Sireno",
    "synopsis": "Mika Jones, una brillante bióloga marina de 25 años, quedó paralizada por un trauma infantil que ya no recuerda. Está a punto de casarse con Victor, el científico obsesionado con cazar a Ilar, el peligroso Príncipe del Océano. Tras un ataque de Victor que deja a Marella, la prometida sirena de Ilar, en muerte cerebral, Mika acepta transferir su conciencia al cuerpo de Marella para infiltrarse en el reino submarino y evitar una guerra. Pero cuanto más se acerca a Ilar, más reacciona el misterioso Heart of the Ocean… y más difícil es separar la misión del deseo. Mientras aprende a sobrevivir en un cuerpo que no es el suyo, recuerdos fragmentados revelan que ella e Ilar ya se habían encontrado. Y Victor y su amante Hanna también tienen planes para Mika, el cuerpo de Marella y el Heart.",
    "posterUrl": "/cdn-proxy/img/movies/55X40vzRwXn7X7BbW3F3BGoH/cover-es.png?v=1790935946360",
    "episodeCount": 9,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-6",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "la-crueldad-de-su-marido-la-empujo-a-los-brazos-de-un-multimillonario",
    "title": "La crueldad de su marido la empujó a los brazos de un multimillonario",
    "synopsis": "Humillada por su esposo, Jake, el día de su boda por seguir siendo virgen, Ruby se coloca una pulsera que detendrá su corazón si desobedece. Sus órdenes la arrastran a los brazos de Alaric Vale, el padre multimillonario de Jake. Con cada nuevo reto, cruzan un límite más, mientras Jake se acerca cada vez más. Pero cuando por fin encuentra a su esposa en brazos de su propio padre, quizá la pulsera ya no sea la razón por la que Ruby se queda.",
    "posterUrl": "/cdn-proxy/img/movies/vnq1C0t2Pl3TWG4sbwD2MUzD/cover-es.png?v=1791285070650",
    "episodeCount": 13,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-7",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "chaqueta-equivocada-chica-indicada-se-lo-que-hiciste-el-ultimo-halloween",
    "title": "Chaqueta equivocada, chica indicada: Sé lo que hiciste el último Halloween",
    "synopsis": "Volvía a casa de mi turno de Halloween con una máscara de zorro cuando una camioneta pickup negra salió de la niebla y atropelló a un hombre disfrazado de oso. La conductora se bajó, se arrodilló a su lado… y se fue. Era Logan McCallahan, quarterback estrella y la chica más fotografiada del estado. Así que dejé una nota en su parabrisas: “Sé lo que hiciste. Dilo. Por favor. Ahora”.\nAhora alguien más está dejando notas, y no dicen “por favor”. El disfraz de oso ha desaparecido, y alguien dentro sabe mi nombre. Y la chica a la que estoy cazando acaba de contarle su secreto más oscuro a un desconocido con máscara de zorro. No tiene ni idea de que era yo.",
    "posterUrl": "/cdn-proxy/img/movies/P2IdfehheWFr231L03thfEqa/cover-es.png?v=1791878247869",
    "episodeCount": 12,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-8",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "mi-jefe-vampiro-sexy-quiere-devorarme",
    "title": "Mi jefe vampiro sexy quiere devorarme",
    "synopsis": "En un laboratorio secreto creado para estudiar y destruir vampiros, la brillante científica Selena ha dedicado su vida a odiar a las criaturas que mataron a su familia… hasta que su arrogante rival Kyle se infecta accidentalmente con sangre vampírica en un experimento que sale mal. Mientras Kyle se precipita hacia la pérdida definitiva de su humanidad, Selena acepta un pacto prohibido para salvarlo, solo para descubrir que no es un vampiro cualquiera: es un Alpha, el más raro y poderoso de su especie. Atrapada entre su sed de venganza y una atracción imposible hacia el hombre que la entrenaron para destruir, Selena deberá elegir entre el veneno que creó para matarlos… y lo único que puede salvarlo: su propia sangre.",
    "posterUrl": "/cdn-proxy/img/movies/Cuw4miG-c4O-2Tiik0-f8WVS/cover-es.png?v=1791291269211",
    "episodeCount": 13,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-9",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "la-carterista-y-el-multimillonario",
    "title": "La carterista y el multimillonario",
    "synopsis": "Lil sabe lo que es sobrevivir en la calle sin depender de nadie. Una noche se cruza con Nathan Sterling, un multimillonario hermético, y le devuelve un reloj carísimo que le habían robado. Impresionado por su honestidad, Nathan le ofrece la oportunidad de empezar de cero. Pronto Lil demuestra que está lejos de ser indefensa: con su rapidez mental y su instinto callejero saca a Nathan de una crisis de alto riesgo, y él le propone un trabajo. A medida que sus mundos se entrelazan, crece una atracción irresistible… pero también el peligro. Muy pronto deberán decidir hasta dónde están dispuestos a llegar para protegerse.",
    "posterUrl": "/cdn-proxy/img/movies/H5AuR2k95u0SDJ4gCU3x_3B9/cover-es.png?v=1791791966416",
    "episodeCount": 10,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-10",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "vendida-por-diez-millones-al-alfa-que-no-la-deja-ir",
    "title": "Vendida por diez millones al Alfa que no la deja ir",
    "synopsis": "Desesperada por salvar a su hermana moribunda, Nancy, de 21 años, vende su virginidad en una subasta secreta de hombres lobo, esperando una sola noche de humillación a cambio del dinero para pagar el hospital. Pero la compran por diez millones de dólares: Mark, un Alfa despiadado y peligrosamente atractivo, que no piensa soltarla.\n\nMark necesita a una virgen humana para un antiguo ritual de Blood Moon que despertará su verdadero poder de Alfa, y hasta que salga la luna, Nancy le pertenece. Ella odia su control, su collar y que la trate como propiedad. Pero cuando hombres lobo rivales empiezan a cazarla y Mark se convierte en el único que la mantiene con vida, Nancy afronta un problema aún peor: cuanto más lucha contra su Alfa captor, más desesperadamente lo desea.",
    "posterUrl": "/cdn-proxy/img/movies/O2Q97BzqhA2gNm7rIBMkoGLm/cover-es.png?v=1791198080426",
    "episodeCount": 12,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-11",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "el-baile-de-medianoche-del-multimillonario",
    "title": "El baile de medianoche del multimillonario",
    "synopsis": "Mia es camarera en un club lleno de vida, donde se atreve a enfrentarse al arrogante Anthony, sin imaginar que así llamará la atención de su enigmático hermano, Lucas. Cuando Lucas interviene para protegerla, entre ellos surge una atracción imposible de ignorar. Pero el mundo de Mia se derrumba cuando, para salvar a su padre, se ve obligada a casarse con el misterioso Charles… sin sospechar que Lucas y Charles son la misma persona.\n",
    "posterUrl": "/cdn-proxy/img/movies/kXoWELF8XuKkVx9jg-RnEXAv/cover-es.png?v=1763636521472",
    "episodeCount": 56,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-12",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "la-trampa-del-ceo",
    "title": "La trampa del CEO",
    "synopsis": "Eva Bennett es una joven agente del FBI enviada en una misión encubierta para seducir y desenmascarar a Adrian Blake, el brillante y frío director ejecutivo de un imperio financiero multimillonario, sospechoso de fraude a gran escala. Se infiltra en su vida como una simple candidata a un puesto de trabajo y rápidamente se convierte en su asistente personal, y mucho más. Pero cuanto más se acerca Eva a los secretos del \"Proyecto X\", más se enreda en sus sentimientos por Adrian. Entre la confianza y la traición, entre el deber y el amor, debe decidir de qué lado está realmente. Porque en este juego, cada error es mortal.",
    "posterUrl": "/cdn-proxy/img/movies/VpbJoXC64doHdGcBC7UGebYc/cover-es.png?v=1764237952119",
    "episodeCount": 45,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-13",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "el-primo-que-no-deberia-amar",
    "title": "El primo que no debería amar",
    "synopsis": "En la víspera de su boda, Isabella descubre la infidelidad de su prometido con su hermanastra y halla refugio en Luca, el primo de él. Entre escándalo, venganza y atracción prohibida, nace una pasión marcada por secretos.",
    "posterUrl": "/cdn-proxy/img/movies/y-gHeuewQtueDt0w9R3kM41_/cover-es.png?v=1763561757050",
    "episodeCount": 49,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-14",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "mi-hermanastro-prohibido",
    "title": "Mi Hermanastro Prohibido",
    "synopsis": "Después de una noche de pasión, Emily y Preston quedan atrapados entre deseo, tabúes y secretos familiares.",
    "posterUrl": "/cdn-proxy/img/movies/RkE-0mgeV1r2frDNclk16ojK/cover.png?v=1755497694807",
    "episodeCount": 60,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  },
  {
    "id": "disc-ds-15",
    "sourceId": "src-7",
    "sourceName": "DramaVivo",
    "externalId": "la-novia-suplente-del-multimillonario",
    "title": "La novia suplente del multimillonario",
    "synopsis": "Elena está atrapada en una situación imposible, dividida entre su amor por Nicholas y una peligrosa proposición de Sebastian, un poderoso director general. Cuando los secretos empiezan a desvelarse y los juegos de poder se intensifican, Elena debe navegar por una red de engaños, pasión y manipulación. Con todo en juego, se ve obligada a tomar una decisión que podría cambiar su vida para siempre. En el mundo de Sebastian, el amor y la traición están estrechamente entrelazados, y Elena pronto se da cuenta de que puede formar parte de un juego mucho mayor.",
    "posterUrl": "/cdn-proxy/img/movies/fd24Jo7iHg8C03Ak3ZueE7Gp/cover.png?v=1750667476143",
    "episodeCount": 64,
    "language": "Español",
    "status": "imported",
    "discoveredAt": "2026-03-01T00:00:00Z"
  }
];

export const MOCK_RIGHTS: RightsRecord[] = [
  {
    "id": "rr-ds-1",
    "seriesId": "ds-1",
    "seriesTitle": "Mi prometido me vendió a dos bestias ardientes",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-2",
    "seriesId": "ds-2",
    "seriesTitle": "¡Mi ex me hizo engordar! Dulce venganza",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-3",
    "seriesId": "ds-3",
    "seriesTitle": "Cada noche llevaba el rostro de su hermana",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-4",
    "seriesId": "ds-4",
    "seriesTitle": "Mi padre me apostó al harén del capo",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-5",
    "seriesId": "ds-5",
    "seriesTitle": "Me convertí en sirena para espiar al Príncipe Sireno",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-6",
    "seriesId": "ds-6",
    "seriesTitle": "La crueldad de su marido la empujó a los brazos de un multimillonario",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-7",
    "seriesId": "ds-7",
    "seriesTitle": "Chaqueta equivocada, chica indicada: Sé lo que hiciste el último Halloween",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-8",
    "seriesId": "ds-8",
    "seriesTitle": "Mi jefe vampiro sexy quiere devorarme",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-9",
    "seriesId": "ds-9",
    "seriesTitle": "La carterista y el multimillonario",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-10",
    "seriesId": "ds-10",
    "seriesTitle": "Vendida por diez millones al Alfa que no la deja ir",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-11",
    "seriesId": "ds-11",
    "seriesTitle": "El baile de medianoche del multimillonario",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-12",
    "seriesId": "ds-12",
    "seriesTitle": "La trampa del CEO",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-13",
    "seriesId": "ds-13",
    "seriesTitle": "El primo que no debería amar",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-14",
    "seriesId": "ds-14",
    "seriesTitle": "Mi Hermanastro Prohibido",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  },
  {
    "id": "rr-ds-15",
    "seriesId": "ds-15",
    "seriesTitle": "La novia suplente del multimillonario",
    "holderName": "DramaVivo Media Group",
    "licenseType": "exclusive",
    "status": "approved",
    "territory": [
      "GLOBAL"
    ],
    "validFrom": "2026-01-01T00:00:00Z",
    "validUntil": "2030-01-01T00:00:00Z",
    "reviewedAt": "2026-01-01T00:00:00Z",
    "reviewedBy": "admin",
    "createdAt": "2026-01-01T00:00:00Z",
    "notes": "Verified and active license"
  }
];

export const MOCK_VIDEOS: VideoAsset[] = [
  {
    "id": "vid-1",
    "filename": "stream_master.m3u8",
    "storagePath": "/vod/prod/hls/",
    "resolution": "1080p",
    "aspectRatio": "9:16",
    "format": "hls",
    "fileSize": 45000000,
    "duration": 90,
    "status": "ready",
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-01-01T00:00:00Z"
  }
];

export const MOCK_TAKEDOWNS: TakedownRequest[] = [];

export const MOCK_ANALYTICS: AnalyticsSummary = {
  "totalViews": 8940000,
  "watchTimeMinutes": 745000,
  "activeUsers": 142000,
  "topSeries": [
    {
      "seriesId": "ds-1",
      "title": "Mi prometido me vendió a dos bestias ardientes",
      "views": 412000
    },
    {
      "seriesId": "ds-2",
      "title": "¡Mi ex me hizo engordar! Dulce venganza",
      "views": 389000
    },
    {
      "seriesId": "ds-3",
      "title": "Cada noche llevaba el rostro de su hermana",
      "views": 365000
    }
  ],
  "trafficByDay": [
    {
      "date": "2026-03-01",
      "views": 28400
    },
    {
      "date": "2026-03-02",
      "views": 31200
    },
    {
      "date": "2026-03-03",
      "views": 35800
    }
  ]
};
