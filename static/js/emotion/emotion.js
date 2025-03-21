window.onload = function () {
   const graphs = [
	   {
		   selector: ".emotion_graph_mm",
		   url: '/emotion/main_data1/',
		   barColor: "#7D7D7D",
		   lineColor: "#001DFF",
	   },
	   {
		   selector: ".emotion_graph_ww",
		   url: "/emotion/main_data2/",
		   barColor: "#7D7D7D",
		   lineColor: "#001DFF",
		   useLabels: true,
	   },
	   {
		   selector: ".family_graph_ll",
		   url: '/emotion/main_data3/',
		   barColor: "#F4A79D",
		   lineColor: null,
			 customYScale: true,
	   },
	   {
		   selector: ".personal_graphh",
		   url: '/emotion/main_data5/',
		   barColor: "#344BFD",
		   barColor2: "#F68D2B",
		   lineColor: null,
		   customYScale: true, // Y축 범위를 동적으로 설정
	   },
	   
   ];

   const commonHeight = 280;
   const padding = 28;

   // 데이터 가져오기
   function fetchData(url) {
	  return fetch(url)
		 .then(response => response.json())
		 .catch(error => {
			console.error("Error fetching data:", error);
			return []; // 오류 발생 시 빈 배열 반환
		 });
   }

   function drawBarChart({ selector, data, barColor, barColor2, lineColor, useLabels = false, customYScale = false }) {
		const container = document.querySelector(selector);
		const svg = d3.select(container).append("svg");
 
		function updateSize() {
			 const width = container.offsetWidth;
			 svg.attr("width", width).attr("height", commonHeight);
 
			 const xScale = d3.scaleBand()
					.rangeRound([padding, width - padding])
					.padding(0.3)
					.domain(data.map(d => d.name));
 
			 const yMax = customYScale ? d3.max(data, d => Math.max(d.value || 0, d.value2 || 0)) * 1.1 : 100;
			 const yScale = d3.scaleLinear()
					.domain([0, yMax])
					.range([commonHeight - padding - 10, padding - 10]);  // 10px 위로 올리기
 
			 svg.selectAll("*").remove();
 
			 // Draw axis
			 const xAxis = d3.axisBottom(xScale).tickSize(0);
			 svg.append("g")
					.attr("transform", `translate(0,${commonHeight - padding + 2})`)
					.call(xAxis);
 
			 svg.selectAll(".tick text")
					.each(function (d) {
						 if (useLabels) {
								const datum = data.find(item => item.name === d);
								const text = d3.select(this);
								text.text("");
 
								text.append("tspan")
								.text(datum.name)
								.attr("x", 0)
								.attr("dy", "0em")
								.attr("class", "value-text");
 
								text.append("tspan")
								.text(datum.label)
								.attr("x", 0)
								.attr("dy", "1em")
						 }
					})
					.attr("transform", "translate(0, 5)");
 
			 svg.selectAll("path.domain").remove();
 
			 // Draw vertical lines
			 svg.selectAll(".vertical-line")
					.data(data)
					.enter()
					.append("line")
					.attr("class", "vertical-line")
					.attr("x1", d => xScale(d.name) + xScale.bandwidth() / 2)
					.attr("x2", d => xScale(d.name) + xScale.bandwidth() / 2)
					.attr("y1", commonHeight - padding)
					.attr("y2", padding);
 
			 // Draw bars
			 svg.selectAll(".bar")
					.data(data.filter(d => d.value > 0)) // value > 0인 데이터만 처리
					.enter()
					.append("rect")
					.attr("class", "bar")
					.attr("x", d => xScale(d.name))
					.attr("y", d => yScale(0)) // yScale(0)을 기준으로 시작
					.attr("width", xScale.bandwidth())
					.attr("height", 0)
					.attr("fill", barColor)
					.attr("rx", 15)
					.attr("ry", 15)
					.transition()
					.duration(800)
					.delay((d, i) => i * 100)
					.ease(d3.easeCubicOut)
					.attr("y", d => yScale(d.value))
					.attr("height", d => Math.max(yScale(0) - yScale(d.value), 0)); // 바의 최종 높이
 
			 // 두 번째 바 (value2)
			 svg.selectAll(".bar2")
					.data(data.filter(d => d.value2 > 0)) // value2 > 0인 데이터만 처리
					.enter()
					.append("rect")
					.attr("class", "bar2")
					.attr("x", d => xScale(d.name))
					.attr("y", d => yScale(0)) 
					.attr("width", xScale.bandwidth()) // 전체 너비로 설정
					.attr("height", 0)
					.attr("fill", barColor2)
					.attr("rx", 15)
					.attr("ry", 15)
					.transition()
					.duration(800)
					.delay((d, i) => i * 100)
					.ease(d3.easeCubicOut)
					.attr("y", d => yScale(d.value2)) // 최종 y 위치
					.attr("height", d => d.value > 0 ? Math.max(yScale(0) - yScale(d.value2), 0) : 0);
 
			 // Draw values
			 svg.selectAll(".value_text")
					.data(data)
					.enter()
					.append("text")
					.attr("class", "value-text")
					.attr("x", d => xScale(d.name) + xScale.bandwidth() / 2)
					.attr("y", padding / 2 )
					.attr("text-anchor", "middle")
					.text(d => d.value)
					.attr('fill', barColor);
 
			 svg.selectAll(".value2_text")
					.data(data)
					.enter()
					.append("text")
					.attr("class", "value2-text")
					.attr("x", d => xScale(d.name) + xScale.bandwidth() / 2)
					.attr("y", d => padding / 2 + 20) // value_text 아래로 위치
					.attr("text-anchor", "middle")
					.text(d => d.value2)
					.attr('fill','#F68D2B');
 
			 // Draw line
			 if (lineColor) {
				const line = d3.line()
						.x(d => xScale(d.name) + xScale.bandwidth() / 2)
						.y(d => yScale(d.value)) // 여기에서 10px 만큼 올린 값을 적용
						.curve(d3.curveMonotoneX); // 부드러운 곡선 추가

 
					const linePath = svg.append("path")
						 .datum(data)
						 .attr("fill", "none")
						 .attr("stroke", lineColor)
						 .attr("stroke-width", 1.2)
						 .attr("d", line);
 
					// 애니메이션 설정
					const totalLength = linePath.node().getTotalLength(); // 라인의 전체 길이 계산
					linePath
						 .attr("stroke-dasharray", `${totalLength} ${totalLength}`) // 대시 배열 설정
						 .attr("stroke-dashoffset", totalLength) // 숨김 상태
						 .transition()
						 .duration(1500)
						 .ease(d3.easeCubicOut)
						 .attr("stroke-dashoffset", 0); // 라인 그려짐
			 }
		}
 
		updateSize();
		window.addEventListener("resize", updateSize);
 }


  // 파이차트 댓글
  function drawPieChart({ selector, data }) {
	  const container = document.querySelector(selector);
	  const width = container.offsetWidth;
	  const height = 280;
	  const radius = Math.min(width, height) / 3;

	  const svg = d3.select(container)
		 .append("svg")
		 .attr("width", width)
		 .attr("height", height + 50)
		 .append("g")
		 .attr("transform", `translate(${width / 2}, 90)`);

	  const color = d3.scaleOrdinal(d3.schemeSet2);
	  const pie = d3.pie().value(d => d.value);
	  const arc = d3.arc().outerRadius(radius - 10).innerRadius(0);

	  const pieData = pie(data);

	  svg.selectAll(".arc")
		 .data(pieData)
		 .enter()
		 .append("g")
		 .attr("class", "arc")
		 .append("path")
		 .attr("d", arc)
		 .attr("fill", (d, i) => color(i));

	  // Add Legend
	  const legend = svg.append("g")
		 .attr("transform", `translate(-${radius - 15}, ${height / 3 + 10})`);

	  const totalValue = d3.sum(data, d => d.value);

	  legend.selectAll(".legend-item")
		 .data(data)
		 .enter()
		 .append("g")
		 .attr("class", "legend-item")
		 .attr("transform", (d, i) => `translate(20, ${i * 25})`)
		 .each(function(d, i) {
			const group = d3.select(this);
			group.append("rect")
			   .attr("x", 0)
			   .attr("width", 15)
			   .attr("height", 15)
			   .attr("fill", color(i));
			   
			const percentage = ((d.value / totalValue) * 100).toFixed(1);
			group.append("text")
			   .attr("x", 20)
			   .attr("y", 12)
			   .text(`${d.name} (${d.value}개)`);
		 });

	  // Resize functionality for Pie chart
	  function updateSize() {
		 const width = container.offsetWidth;
		 const height = 280;
		 const radius = Math.min(width, height) / 3;

		 svg.attr("width", width).attr("height", height + 80);

		 svg.selectAll("path")
			.attr("d", arc.outerRadius(radius - 10).innerRadius(0));
	  }

	  window.addEventListener("resize", updateSize);
	  updateSize(); // Initial size adjustment
   }


   // 데이터 가져와서 그래프 그리기
   function loadGraphsData() {
	  const pieDataUrl = "/emotion/main_data4/"; // 예시 데이터 URL
	  const pieData = fetchData(pieDataUrl);

	  pieData.then(data => {
			drawPieChart({ selector: ".family_graph_rr", data: data });
	  });

	  graphs.forEach(graph => {
			fetchData(graph.url).then(data => {
			   drawBarChart({
				  selector: graph.selector,
				  data: data,
				  barColor: graph.barColor,
				  barColor2: graph.barColor2,
				  lineColor: graph.lineColor,
				  useLabels: graph.useLabels,
				  customYScale: graph.customYScale || false // customYScale 값을 전달
			   });
			});
	  });
   }

  loadGraphsData();
};

