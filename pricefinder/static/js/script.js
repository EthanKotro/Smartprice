async function fetchBestDeal() {
    const query = document.getElementById("searchInput").value;
    if (!query) {
        alert("Please enter a product name.");
        return;
    }

    try {
        const response = await fetch(`/api/best-deal?q=${query}`);
        const data = await response.json();

        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById("result").innerHTML = `
                <h2>Best Deal: ${data.name}</h2>
                <p>Store: ${data.store}</p>
                <p>Price: KES ${data.price}</p>
                <a href="${data.url}" target="_blank">View Product</a>
                <br>
                <img src="${data.image_url}" alt="${data.name}" style="width: 150px;">
            `;
        }
    } catch (error) {
        console.error("Error fetching best deal:", error);
    }
}
