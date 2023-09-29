<script lang="ts">
	import { onMount } from 'svelte';
	import type { DatasetInfo } from '$lib/types/dataset_info';
	import { LogarithmicScale } from 'chart.js';
	import Tendencia from '$lib/components/tendencia.svelte';
	import Piechart from '$lib/components/piechart.svelte';
	import '../styles/style.css';
	import Icon from '../assets/img/git.png';

	let datasetInfo: DatasetInfo;

	let valorSelect: string = '13';

	let tendenciaData: Promise<any> = getDummyData(valorSelect);

	async function getDummyData(fechaSesion: string): Promise<any> {
		const API_URL = `http://127.0.0.1:8000/eventos/${fechaSesion}`;

		const response = await fetch(API_URL);
		const jsonData = await response.json(); // Espera la respuesta y el JSON

		const transposedData = jsonData.columns.map((column: string, columnIndex: number) => ({
			label: column,
			data: jsonData.data.map((row: any[], rowIndex: number) => ({
				x: jsonData.index[rowIndex],
				y: row[columnIndex]
			})),
			hoverBackgroundColor: 'rgb(0, 255, 0)'
		}));

		// console.log(jsonData);
		// console.log(transposedData);
		//tendenciaData = transposedData;
		return transposedData;
	}

	async function updateData(): Promise<void> {
		tendenciaData = getDummyData(valorSelect);
		pieChartData = getPieChartData(valorSelect);
		await obtenerDatos();
		await obtenerMenorTiempo();
		// console.log(valorSelect);
	}

	let pieChartData = getPieChartData(valorSelect);

	async function getPieChartData(fechaSesion: string): Promise<any> {
		const API_URL = `http://127.0.0.1:8000/asistencia/${fechaSesion}`;

		const response = await fetch(API_URL);
		const jsonData = await response.json(); // Espera la respuesta y el JSON

		const dataArray = Object.values(jsonData);

		// console.log(dataArray);

		return dataArray;
	}

	let total: number = 0;
	let promedio: number = 0;
	let std: number = 0;

	async function obtenerDatos() {
		const response = await fetch(`http://127.0.0.1:8000/analisis/${valorSelect}`);
		const jsonData = await response.json();

		total = jsonData.total;
		promedio = jsonData.promedio;
		std = jsonData.std;
	}
	onMount(obtenerDatos);

	let nombreCompleto: string = '';
	let correo: string = '';
	let duracion: number = 0;

	async function obtenerMenorTiempo() {
		const response = await fetch(`http://127.0.0.1:8000/menor_tiempo/${valorSelect}`);
		const jsonData = await response.json();

		const id = Object.keys(jsonData)[0]; // Obtener la clave (por ejemplo, "38")
		const item = jsonData[id];
		nombreCompleto = item.nombre_completo;
		correo = item.correo;
		duracion = item.duración;

		// Puedes hacer lo que necesites con estos valores aquí
		// console.log('ID:', id);
		// console.log('Nombre completo:', nombreCompleto);
		// console.log('Correo:', correo);
		// console.log('Duración:', duracion);
	}
	onMount(obtenerMenorTiempo);
</script>

<div class="container">
	<header class="headercyber">
		<h1 class="headercyber__title">CyberSecurity Attendance Analytics</h1>
		<nav>
			<div class="event">
				<label for="event-selector" id="label-selector" class="event__title">
					Selecciona un Evento <br />
					<span class="event__click">Dando Click</span>
				</label>
				<select
					id="evento-selector"
					class="event__select"
					bind:value={valorSelect}
					on:change={() => {
						void updateData();
					}}
				>
					<option value="06">Evento 06</option>
					<option value="08">Evento 08</option>
					<option value="13">Evento 13</option>
					<option value="15">Evento 15</option>
				</select>
			</div>
		</nav>
	</header>

	<div class="cardmain">
		<div class="cardmain__card">
			<div class="cardmain__card--hover" />
			<h2 class="card__number">{total}</h2>
			<h2 class="card__title">Número de Asistentes</h2>
		</div>

		<div class="cardmain__card">
			<div class="cardmain__card--hover" />
			<h2 class="card__number">{promedio}</h2>
			<h2 class="card__title">Duración promedio</h2>
		</div>

		<div class="cardmain__card">
			<div class="cardmain__card--hover" />
			<h2 class="card__number">{std}</h2>
			<h2 class="card__title">Desviación estandar de la duración</h2>
		</div>

		<div class="cardmain__card">
			<div class="cardmain__card--hover" />
			<span class="card__duration"
				>{nombreCompleto}<br />{correo}<br />Duración:
				<strong class="card__number">{duracion}</strong> min.</span
			>
			<span class="card__duration--title">Menor Tiempo</span>
		</div>

		<!-- Agrega más tarjetas si es necesario -->
	</div>

	<div class="graphics">
		<div class="graphics__card">
			{#await tendenciaData}
				<p>Loading...</p>
			{:then tendenciaData}
				<!-- <p>Listos:</p> -->
				<Tendencia transposedData={tendenciaData} />
			{/await}
		</div>
		<div class="graphics__card">
			{#await pieChartData}
				<p>Loading...</p>
			{:then pieChartData}
				<!-- <p>Listos:</p> -->
				<Piechart dataArray={pieChartData} />
			{/await}
		</div>
	</div>
	<footer class="footer">
		<div class="footer--center">
			<p class="footer__name">Juan Sebastian Mora Tibamoso</p>
			<p class="footer__email">juan.mora02@uptc.edu.co</p>
			<a class="footer__credits" href="https://github.com/JSEB99" target="_blank">
				<img src={Icon} alt="github" class="footer__icon" />
			</a>
		</div>
	</footer>
</div>
