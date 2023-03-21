const displayAddressData = (addressData) => {
    // Render the address data in the UI
    const addressDiv = document.createElement('div');
    addressDiv.innerHTML = `
      <h2>${addressData.address}</h2>
      <p>Postal Code: ${addressData.postal_code}</p>
      <p>Area: ${addressData.area}</p>
      <p>District: ${addressData.district}</p>
    `;
    document.body.appendChild(addressDiv);
  };
  
  // Send a POST request to the GraphQL API
  fetch('/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: '{ address(address: "123 Main St") { address, postal_code, area, district } }' }),
  })
    .then(response => response.json())
    .then(data => {
      // Render the address data in the UI
      const addressData = data.data.address;
      displayAddressData(addressData);
    });
  