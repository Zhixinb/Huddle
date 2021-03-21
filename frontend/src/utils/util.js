function generate_lines(s_id, c_id, slides) {
    const connections = slides[s_id]["connections"]
    const components = slides[s_id]["components"]
    var queue = []
    if (c_id in components) {
        queue.push(c_id)
    }
    var lines = []
    while (queue.length > 0) {
        const start_c_id = queue.shift()
        const x0 = components[start_c_id].x
        const y0 = components[start_c_id].y
        if (start_c_id in connections) {
            for (const signal in connections[start_c_id]) {
                for (const end_c_id in connections[start_c_id][signal]) {
                    if (Object.keys(connections[start_c_id][signal][end_c_id]).length > 0) {
                        queue.push[end_c_id]
                        const x1 = components[end_c_id].x
                        const y1 = components[end_c_id].y
                        lines.push([x0, y0, x1, y1])
                    }
                }
            }
        }
    }
    return lines;
}
export {
    generate_lines
}