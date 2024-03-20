# Block Chain

To run the client in docker:

1. Open the console in this directory

2. run command

   ```
   docker build -t block-chain .
   ```

   This command uses the Docker File to initialize a container.

3. run command

   ```
   docker run --rm -d --network host block-chain
   ```

   --rm can be removed. It will automatically clear the container once you stop it.

   --network host makes sure that the broad cast sent by the container can be listened by the local host.

