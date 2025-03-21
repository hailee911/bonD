// 서버에서 가족 구성원 데이터를 받아옵니다.
fetch('/main/get_family_members/')
.then(response => response.json())
.then(data => {
    // 가족 구성원 이름을 동적으로 추가
    const familyMembersContainer = document.getElementById('family-members');
    data.forEach((member, index) => {
        const div = document.createElement('div');
        div.classList.add('person-name');
        div.textContent = member.name;
        div.onclick = () => {
            // 선택된 구성원의 감정 그래프 로드
            loadEmotionGraph(member.id);
            
            // 모든 이름 글씨를 기본 상태로 설정
            const allMembers = document.querySelectorAll('.person-name');
            allMembers.forEach(item => {
                item.style.fontSize = '18px';  // 기본 글씨 두께로 설정
                item.style.fontWeight = '400';  // 기본 글씨 두께로 설정
                item.style.color = '#797979';  // 기본 글씨 두께로 설정
                item.style.background = '#fff';  // 기본 글씨 두께로 설정
            });
            
            // 선택된 구성원 글씨를 bold로 설정
            div.style.fontWeight = '600';
            div.style.color = '#222';
            div.style.background = '#eeeeee';
        };

        familyMembersContainer.appendChild(div);

        // 첫 번째로 내 감정 그래프 자동 로드
        if (index === 0) {
					loadEmotionGraph(member.id);  // 페이지 로드 시 첫 번째로 감정 그래프 자동 로드
					div.style.fontWeight = '600';  // 내 이름을 첫 번째로 표시하며 글씨를 bold로 설정
					div.style.color = '#222';  // 내 이름의 글씨 색상을 black으로 설정
					div.style.background = '#eeeeee';
				} else {
						div.style.fontWeight = 'normal';  // 나머지 이름은 기본 글씨 두께
						div.style.color = '#999';  // 나머지 이름은 기본 글씨 색상
				}
    });
})
.catch(error => console.error('Error fetching family members:', error));


// 감정 그래프를 그리는 함수 (D3.js 활용)
function drawBarChart({ selector, data, barColor, lineColor, useLabels = false, customYScale = false, barBottomPadding = -30 }) {
	const container = document.querySelector(selector);
	const padding = 30;
	const commonHeight = 348; // 그래프 높이
	const svg = d3.select(container).select("svg");

	svg.selectAll("*").remove();

	const width = container.offsetWidth;
	svg.attr("width", width).attr("height", commonHeight);

	const xScale = d3.scaleBand()
									.rangeRound([padding, width - padding])
									.padding(0.5)
									.domain(data.map(d => d.name));

	const yMax = customYScale ? 100 : 100;
	const yScale = d3.scaleLinear()
									.domain([0, yMax])
									.range([commonHeight - padding - 20 + barBottomPadding, padding]);  // 그래프가 상단으로 오게

	// 세로 그리드 추가
	svg.selectAll(".vertical-grid")
	.data(data)
	.enter()
	.append("line")
	.attr("class", "vertical-grid")
	.attr("x1", d => xScale(d.name) + xScale.bandwidth() / 2)
	.attr("x2", d => xScale(d.name) + xScale.bandwidth() / 2)
	.attr("y1", padding)
	.attr("y2", commonHeight - padding + barBottomPadding)
	.attr("stroke", "#ddd")
	.attr("stroke-width", 1)
	.attr("stroke-dasharray", "2,2");

	
	const xAxis = d3.axisBottom(xScale).tickSize(1);
	svg.append("g")
			.attr("transform", `translate(0,${commonHeight - padding + barBottomPadding})`)  // barBottomPadding 반영
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
									.attr("class", "value-text")
									.style("font-size", "15px")
									.style("font-weight", "normal")
									.style("color", "#797979");

							text.append("tspan")
									.text(datum.label)
									.attr("x", 0)
									.attr("dy", "1.2em")
									.style("font-size", "18px")
									.style("font-weight", "600")
									.style("color", "#222");
					}
			})
			.attr("transform", "translate(0, 5)");

	svg.selectAll("path.domain").remove();

	// 막대 그리기
	svg.selectAll(".bar")
			// .data(data)
			// .enter()
			// .append("rect")
			// .attr("class", "bar")
			// .attr("x", d => xScale(d.name))
			// .attr("x", d => xScale(d.name) + (xScale.bandwidth() - 16) / 2)
			// .attr("y", d => d.value > 0 ? yScale(d.value) : yScale(0))  // 0 값 처리
			// .attr("width", 18)
			// //.attr("width", xScale.bandwidth())
			// .attr("height", d => d.value > 0 ? Math.max(yScale(0) - yScale(d.value), 0) : 0)  // 0값 처리, 아래로 길어지지 않도록 수정
			// .attr("fill", barColor)
			// .attr("rx", 10)
			// .attr("ry", 10)
			.data(data)
			.enter()
			.append("rect")
			.attr("class", "bar")
			.attr("x", d => xScale(d.name) + (xScale.bandwidth() - 16) / 2) // 막대의 중심 정렬
			.attr("y", yScale(0)) // 초기 위치를 그래프 바닥으로 설정
			.attr("width", 18) // 막대의 너비 설정
			.attr("height", 0) // 초기 높이를 0으로 설정
			.attr("fill", barColor)
			.attr("rx", 10) // 둥근 모서리 반지름
			.attr("ry", 10)
			.transition() // 애니메이션 시작
			.delay((d, i) => i * 100) // 각 막대에 지연 시간 추가
			.duration(800) // 애니메이션 지속 시간 (밀리초 단위)
			.ease(d3.easeCubicOut) // 애니메이션의 속도 변화 설정
			.attr("y", d => d.value > 0 ? yScale(d.value) : yScale(0)) // 최종 y 위치
			.attr("height", d => d.value > 0 ? Math.max(yScale(0) - yScale(d.value), 0) : 0); // 최종 높이

	// 라인 그리기
	if (lineColor) {
			// const line = d3.line()
			// 		.x(d => xScale(d.name) + xScale.bandwidth() / 2)
			// 		.y(d => yScale(d.value));

			// svg.append("path")
			// 		.datum(data)
			// 		.attr("fill", "none")
			// 		.attr("stroke", lineColor)
			// 		.attr("stroke-width", 1)
			// 		.attr("d", line);
			const line = d3.line()
        .x(d => xScale(d.name) + xScale.bandwidth() / 2)
        .y(d => yScale(d.value))
				.curve(d3.curveMonotoneX); // 부드러운 곡선 추가

			const linePath = svg.append("path")
					.datum(data)
					.attr("fill", "none")
					.attr("stroke", lineColor)
					.attr("stroke-width", 2)
					.attr("d", line);

			// 애니메이션 설정
			const totalLength = linePath.node().getTotalLength(); // 라인의 전체 길이 계산

			linePath
					.attr("stroke-dasharray", `${totalLength} ${totalLength}`) // 대시 배열 설정 (라인 길이만큼)
					.attr("stroke-dashoffset", totalLength) // 대시 오프셋을 전체 길이로 설정 (숨김 상태)
					.transition() // 애니메이션 시작
					.duration(1500) // 애니메이션 지속 시간 (밀리초 단위)
					.ease(d3.easeCubicOut) // 애니메이션의 속도 변화 설정
					.attr("stroke-dashoffset", 0); // 오프셋을 0으로 줄여 라인이 그려지도록 설정
	}
}

// 감정 그래프를 그리는 함수 (D3.js 활용)
function loadEmotionGraph(memberId) {
    const graphContainer = document.getElementById('emotion-graph'); // 그래프를 렌더링할 div
    fetch(`/main/get_emotion_graph/${memberId}/`)  // 서버에서 감정 데이터 요청
        .then(response => response.json())
        .then(data => {
            // 그래프 컨테이너 초기화
            graphContainer.innerHTML = '<svg></svg>';
            drawBarChart({
                selector: "#emotion-graph",
                data: data,
                barColor: "#5881F7",
                lineColor: "#5DCDEF", // 원하는 라인 색상
                useLabels: true,
                customYScale: true
            });
        })
        .catch(error => console.error('Error fetching emotion data:', error));
}
