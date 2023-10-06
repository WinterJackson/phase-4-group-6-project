import React, { useState, useEffect } from "react";
import { Navigate, useParams } from "react-router-dom";
import NewReview from "./NewReview";

function DogHouseDetails() {
    const { id } = useParams();
    const [dogHouse, setDogHouse] = useState(null);
    // const navigate = Navigate();

    // const handleNewReview = () => {
    //     navigate("/reviews")
    // }

    useEffect(() => {
        // Fetch the details of the specific doghouse by ID from the API
        fetch(`/dog_houses/${id}`)
            .then((response) => response.json())
            .then((data) => setDogHouse(data))
            .catch((error) => console.error("Error fetching data:", error));
        }, [id]);

    if (!dogHouse) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>{dogHouse.name}</h2>
                <p>Location: {dogHouse.location}</p>
                <p>Description: {dogHouse.description}</p>
                <img src={dogHouse.image} alt={dogHouse.name} />

            <h3>Reviews</h3>
            <ul>
                {dogHouse.reviews.map((review) => (
                <li key={review.id}>
                    <p>Rating: {review.rating}</p>
                    <p>Content: {review.content}</p>
                </li>
                ))}
            </ul>

            <NewReview />
        </div>
    );
}

export default DogHouseDetails;

// onClick={handleNewReview}