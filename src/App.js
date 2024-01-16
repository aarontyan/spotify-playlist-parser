import React, { useState, useEffect } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Card} from 'react-bootstrap';

function App() {

  const [playlists, setPlaylists] = useState([]);

  useEffect(() => {
    fetch("/playlists").then(
      res => res.json()
    ).then(
      playlists => {
        setPlaylists(playlists.items);
      }
    )
  }, []);


  console.log(playlists)

  return (

    <div className="App">
      <Container>
        <Row className="mx-2 row row-cols-4">
          {playlists.map( (playlist, i)  => {
            console.log(playlist);
            return (
              <Card>
                <Card.Img src={playlist.images[0].url} />
                <Card.Body>
                  <Card.Title>{playlist.name}</Card.Title>
                </Card.Body>
              </Card>
            )
          })}
        </Row>
      </Container>
    </div>
  );
}

export default App