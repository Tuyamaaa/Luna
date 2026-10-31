
document.addEventListener("DOMContentLoaded", function () {

    const categoryFilter = document.getElementById("categoryFilter");
    const sizeFilter = document.getElementById("sizeFilter");
    const priceFilter = document.getElementById("priceFilter");
    const sortFilter = document.getElementById("sortFilter");
    const productSearch = document.getElementById("productSearch");

    const productGrid = document.getElementById("productGrid");
    const productCount = document.getElementById("productCount");
    const noProducts = document.getElementById("noProducts");

    const products = Array.from(
        document.querySelectorAll(".shop-product-card")
    );

    // Бараа бүрийн үнийг уншигдах формат руу хувиргах
    products.forEach(product => {
        const price = Number(product.dataset.price);
        const priceElement = product.querySelector(".shop-price");

        priceElement.textContent = "₮" + price.toLocaleString("en-US");
    });

    function filterProducts() {

        const category = categoryFilter.value;
        const size = sizeFilter.value;
        const priceRange = priceFilter.value;
        const sort = sortFilter.value;
        const search = productSearch.value.toLowerCase().trim();

        let visibleProducts = products.filter(product => {

            const productName = product.dataset.name.toLowerCase();
            const productCategory = product.dataset.category;
            const productPrice = Number(product.dataset.price);

            const productSizes = product.dataset.sizes
                .split(",")
                .filter(Boolean);

            // Category
            const matchCategory =
                category === "all" ||
                productCategory === category;

            // Size
            const matchSize =
                size === "all" ||
                productSizes.includes(size);

            // Price
            let matchPrice = true;

            if (priceRange === "under150") {
                matchPrice = productPrice < 150000;
            }
            else if (priceRange === "150to200") {
                matchPrice =
                    productPrice >= 150000 &&
                    productPrice <= 200000;
            }
            else if (priceRange === "over200") {
                matchPrice = productPrice > 200000;
            }

            // Search
            const matchSearch = productName.includes(search);

            return matchCategory &&
                   matchSize &&
                   matchPrice &&
                   matchSearch;
        });

        // Sorting
        if (sort === "low") {
            visibleProducts.sort(
                (a, b) => Number(a.dataset.price) -
                          Number(b.dataset.price)
            );
        }
        else if (sort === "high") {
            visibleProducts.sort(
                (a, b) => Number(b.dataset.price) -
                          Number(a.dataset.price)
            );
        }
        else if (sort === "name") {
            visibleProducts.sort(
                (a, b) => a.dataset.name.localeCompare(b.dataset.name)
            );
        }
        else {
            visibleProducts.sort(
                (a, b) => Number(a.dataset.id) -
                          Number(b.dataset.id)
            );
        }

        // Бүх бүтээгдэхүүнийг түр нуух
        products.forEach(product => {
            product.hidden = true;
        });

        // Шүүсэн бүтээгдэхүүнийг дарааллаар нь харуулах
        visibleProducts.forEach(product => {
            product.hidden = false;
            productGrid.appendChild(product);
        });

        productCount.textContent =
            visibleProducts.length + " products";

        noProducts.hidden = visibleProducts.length !== 0;
    }

    // Dropdown болон хайлтын event
    categoryFilter.addEventListener("change", filterProducts);
    sizeFilter.addEventListener("change", filterProducts);
    priceFilter.addEventListener("change", filterProducts);
    sortFilter.addEventListener("change", filterProducts);
    productSearch.addEventListener("input", filterProducts);

    // URL-аас category унших:
    // /shop/?category=Bags
    const params = new URLSearchParams(window.location.search);
    const initialCategory = params.get("category");

    if (initialCategory &&
        ["Clothing", "Bags", "Shoes"].includes(initialCategory)) {
        categoryFilter.value = initialCategory;
    }

    filterProducts();
});
