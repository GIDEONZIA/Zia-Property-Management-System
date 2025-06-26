document.addEventListener('DOMContentLoaded', function () {
    // Highlight the residence table rows on hover
    const rows = document.querySelectorAll('table tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.backgroundColor = '#f0f8ff';
        });
        row.addEventListener('mouseleave', () => {
            row.style.backgroundColor = '';
        });
    });

    // Add click event to show residence details in an alert
    rows.forEach(row => {
        row.addEventListener('click', () => {
            const cells = row.querySelectorAll('td');
            const name = cells[0].textContent;
            const address = cells[1].textContent;
            const type = cells[2].textContent;
            const owner = cells[3].textContent;
            alert(
                `Residence: ${name}\nAddress: ${address}\nType: ${type}\nOwner: ${owner}`
            );
        });
    });

    // Add a button to toggle visibility of each section
    const sectionTitles = document.querySelectorAll('h2');
    sectionTitles.forEach(title => {
        const button = document.createElement('button');
        button.textContent = 'Toggle';
        button.style.marginLeft = '10px';
        title.after(button);

        const nextUl = title.nextElementSibling;
        button.addEventListener('click', () => {
            if (nextUl && nextUl.tagName === 'UL') {
                nextUl.style.display = nextUl.style.display === 'none' ? '' : 'none';
            }
        });
    });
});