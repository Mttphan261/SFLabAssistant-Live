import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Row, Col, Container } from "react-bootstrap";


function VideoForm({ handleAddVideo }) {
  const [youtubeLink, setYoutubeLink] = useState("");
  const [videoInfo, setVideoInfo] = useState(null);
  const { name } = useParams();
  const [fighter, setFighter] = useState(null);
  const [videoError, setVideoError] = useState(null);


  useEffect(() => {
    fetch(`/api/characters/${name}`)
      .then((r) => r.json())
      .then((data) => {
        setFighter(data);
      });
  }, [name]);

  useEffect(() => {
    let alertTimeout;

    if (videoInfo) {
      alertTimeout = setTimeout(() => {
        setVideoInfo(null);
        setVideoError(null);
      }, 5000);

      return () => clearTimeout(alertTimeout)
    }
  }, [videoInfo])

  const getYoutubeVideo = (videoLink) => {
    const url = new URL(videoLink);
    const getVideoID = url.searchParams.get("v");
    return getVideoID;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const videoID = getYoutubeVideo(youtubeLink);
    console.log(videoID)
    console.log(fighter.id)

    const data = {
        character_id: fighter.id,
        video_id: videoID
    }

    try {
        const response = await fetch('/api/videos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            const video = await response.json();
            console.log('Video submitted:', video)

            const characterResponse = await fetch(`/api/characters/${name}`)
            const updatedFighter = await characterResponse.json()
            setFighter(updatedFighter)
            handleAddVideo(video)
            setVideoInfo(video)
            setYoutubeLink("")
        } else {
            console.error('Video submission failed', response.status)
            setVideoError(true)
        } 
    } catch (error) {
        console.error('Video submission failed:', error)
        setVideoError(true)
    }
  }

  return (
    <Row>
      <form onSubmit={handleSubmit}>
        <label style={{
          marginRight: '1%',
          marginBottom: '2%'
        }}>
          Add video to fighter library:
          <input
            type="text"
            placeholder="Paste YouTube link..."
            value={youtubeLink}
            onChange={(e) => setYoutubeLink(e.target.value)}
            className="form-control"
          />
        </label>
        <button type="submit">Submit</button>
      </form>
      {videoInfo && (
        <div className="alert alert-success" role="alert">
          Video added to the fighter library.
        </div>
      )}
      {videoError && (
        <div className="alert-alert-danger" role="alert">
          Failed to add video - make sure it is a valid YouTube link.
        </div>
      )}
    </Row>
  );
}

export default VideoForm;
