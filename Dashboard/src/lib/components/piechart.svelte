<script lang="ts">
	import Chart from 'chart.js/auto';
	import { onMount } from 'svelte';

	// Define el tipo para tus datos
	type DataItem = {
		programa_academico: string;
		cantidad_personas: number;
	};

	export let dataArray: Array<DataItem>;
	let dataArray2: Array<DataItem>;

	// Copia los datos de dataArray a dataArray2 en cada cambio de dataArray
	$: {
		dataArray2 = dataArray.slice();
	}

	let ctx: CanvasRenderingContext2D;
	let canvas: HTMLCanvasElement;

	function createChart() {
		ctx = canvas.getContext('2d')!;
		new Chart(ctx, {
			type: 'pie',
			data: {
				labels: dataArray2.map((row) => row.programa_academico),
				datasets: [
					{
						label: 'Cantidad de personas',
						data: dataArray2.map((row) => row.cantidad_personas),
						hoverOffset: 4
					}
				]
			},
			options: {
				plugins: {
					legend: {
						labels: {
							color: 'rgb(255,255,255)'
						}
					},
					title: {
						display: true,
						text: 'Personas por programa',
						color: 'rgb(255,255,255)'
					}
				}
			}
		});
	}

	// Llama a createChart() una vez que el componente se monta en el DOM
	onMount(createChart);
</script>

<div class="chart-container">
	<canvas bind:this={canvas} />
</div>

<style>
	.chart-container {
		width: 560px;
		height: 350px;
		display: flex;
		justify-content: center;
	}
</style>
