CREATE TABLE Captured (
    Id          SERIAL PRIMARY  KEY,
    PlateNumber VARCHAR(50)          NULL,
    Image       BYTEA                NULL,
    LOCATION    VARCHAR(255)         NOT NULL,
    DateTimeCaptured TIMESTAMP       NOT NULL,
    IsActive    BOOLEAN              NULL
)