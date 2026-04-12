// 1. Trova tutti i link nella pagina e filtra solo quelli che portano a un PDF
const allLinks = Array.from(document.querySelectorAll('a'));
const pdfLinks = allLinks
    .map(a => a.href)
    .filter(href => href.toLowerCase().includes('.pdf'));

// 2. Rimuovi eventuali link duplicati
const uniquePdfLinks = [...new Set(pdfLinks)];

console.log(`Trovati ${uniquePdfLinks.length} PDF unici. Inizio il download...`);

// 3. Scarica i file con un piccolo ritardo tra uno e l'altro
uniquePdfLinks.forEach((link, index) => {
    setTimeout(() => {
        const a = document.createElement('a');
        a.href = link;
        
        // Cerca di impostare il nome del file dall'URL
        const fileName = link.split('/').pop().split('?')[0]; 
        a.download = fileName || `kill_team_file_${index}.pdf`;
        a.setAttribute('target', '_blank'); // Aiuta in alcuni browser
        
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        console.log(`Richiesta di download inviata per ${index + 1}/${uniquePdfLinks.length}: ${a.download}`);
    }, index * 1500); // 1500 millisecondi (1.5 secondi) di pausa tra ogni download
});