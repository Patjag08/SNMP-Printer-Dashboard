async function loadProducts() {

    const response = await fetch('printers.json');
    const products = await response.json();

    return products;
}

function sleep(s) {
  return new Promise(resolve => setTimeout(resolve, s * 1000));
}


document.addEventListener("DOMContentLoaded", () => {
  console.log("table.js running — DOM is ready");
  Main();
});


async function Main() {
    console.log('Loaded');

    let productData;
    while (true) {
        // code block to be executed
        loadProducts().then(data => {
            productData = data; // assign the loaded data to a variable
            console.log("Products loaded:", productData);
            const table_body = document.getElementById('table-body');
            table_body.innerHTML = "";
            // This is for the index specificly
            productData.forEach((item, index) => {
                const printer = document.createElement('tr');
                printer.innerHTML = `
                    <th scope="row">${item.IP}</th>
                    <td>${item.Serial_number}</td>
                    <td>${item.name}</td>
                    <td>${item.Black_toner}</td>
                    <td>${item.Cyan_toner}</td>
                    <td>${item.Magenta_toner}</td>
                    <td>${item.Yellow_toner}</td>
                    <td>${item.Print_count}</td>
                `.trim();
                table_body.appendChild(printer);
            });
        });
        await sleep(60);
    }
}