// frontend/src/App.js
import React, { useState } from 'react';
import {Container} from 'react-bootstrap';
import MappingPage from "./catmapping";
import ImportPage from "./loadtransactions";


function App() {
  const [isCatVisible, setCatVisible] = useState(false);
  const [isImportVisible, setImportVisible] = useState(false);

  return (
      <Container>
        <button onClick={() => setCatVisible(!isCatVisible)}>Показать/Скрыть MappingPage</button>
        {isCatVisible && <MappingPage/>}
        <br/><br/>
        <button onClick={() => setImportVisible(!isImportVisible)}>Показать/Скрыть Раздел импорта</button>
        {isImportVisible && <ImportPage/>}
        <br/><br/>
      </Container>
  );
}

export default App;
