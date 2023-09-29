<script lang="ts">
	import Chart from 'chart.js/auto';
	import 'chartjs-adapter-date-fns';
	import { onMount } from 'svelte';

	export let transposedData: any;
	let transposedData2: any;
	$: {
		transposedData2 = transposedData;
	}

	let ctx: CanvasRenderingContext2D;
	let canvas: HTMLCanvasElement;
	function createChart() {
		//const transposedData = getDummyData();
		ctx = canvas.getContext('2d')!;
		new Chart(ctx, {
			type: 'line',
			data: {
				datasets: transposedData2 // Utiliza la variable aquí
			},
			options: {
				plugins: {
					legend: {
						labels: {
							color: 'rgb(255, 255, 255)'
						}
					},
					title: {
						display: true,
						text: 'Personas por tiempo por programa',
						color: 'rgb(255,255,255)'
					}
				},
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'hour',
							displayFormats: {
								minute: 'HH:mm'
							}
						},
						title: {
							display: true,
							text: 'Tiempo',
							color: 'rgb(255,255,255)'
						},
						ticks: {
							color: 'rgb(255,255,255)'
						}
					},
					y: {
						title: {
							display: true,
							text: 'Valor',
							color: 'rgb(255,255,255)'
						},
						ticks: {
							color: 'rgb(255,255,255)'
						}
					}
				}
			}
		});
	}

	onMount(createChart);
</script>

<div class="chart-container">
	<canvas bind:this={canvas} />
</div>

<style>
	:global(body) {
		padding: 0;
	}
	.chart-container {
		width: 540px;
		height: 350px;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
