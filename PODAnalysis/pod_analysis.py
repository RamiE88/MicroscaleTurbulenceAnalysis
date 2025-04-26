import numpy as np

def perform_pod_analysis(memmap_file, output_file, num_modes=None):
    """
    Perform Proper Orthogonal Decomposition (POD) on a 3D velocity field from CFD.

    Parameters:
        memmap_file (str): Path to the memory-mapped .npy file containing the velocity dataset.
        output_file (str): Path to save the POD modes and singular values.
        num_modes (int, optional): Number of POD modes to retain. If None, all modes are retained.

    The dataset is assumed to have the shape (nx, ny, nz, n_samples, 3), where:
        - nx, ny, nz: Spatial dimensions of the velocity field.
        - n_samples: Number of time steps or snapshots.
        - 3: Velocity components (u, v, w).
    """
    # Load the memory-mapped dataset
    print("Loading memory-mapped dataset...")
    velocity_data = np.load(memmap_file, mmap_mode='r')

    # Ensure the dataset has the correct shape
    if velocity_data.ndim != 5 or velocity_data.shape[-1] != 3:
        raise ValueError("The dataset must have the shape (nx, ny, nz, n_samples, 3).")

    # Extract dimensions
    nx, ny, nz, n_samples, _ = velocity_data.shape

    # Reshape the data to 2D: (n_samples, n_features), where n_features = nx * ny * nz * 3
    print("Reshaping the data...")
    reshaped_data = velocity_data.reshape(nx * ny * nz * 3, n_samples).T

    # Compute the mean and subtract it to center the data
    print("Centering the data...")
    mean_velocity = np.mean(reshaped_data, axis=0)
    centered_data = reshaped_data - mean_velocity

    # Perform Singular Value Decomposition (SVD)
    print("Performing Singular Value Decomposition (SVD)...")
    U, S, Vt = np.linalg.svd(centered_data, full_matrices=False)

    # Retain only the specified number of modes
    if num_modes is not None:
        print(f"Retaining the first {num_modes} modes...")
        U = U[:, :num_modes]
        S = S[:num_modes]
        Vt = Vt[:num_modes, :]

    # Save the results
    print("Saving POD results...")
    np.savez(output_file, U=U, S=S, Vt=Vt, mean_velocity=mean_velocity, shape=(nx, ny, nz, 3))
    print(f"POD analysis complete. Results saved to {output_file}.")

if __name__ == "__main__":
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Perform POD analysis on a 3D velocity field from CFD.")
    parser.add_argument("memmap_file", type=str, help="Path to the memory-mapped .npy file.")
    parser.add_argument("output_file", type=str, help="Path to save the POD results.")
    parser.add_argument("--num_modes", type=int, default=None, help="Number of POD modes to retain (default: all).")
    args = parser.parse_args()

    # Perform POD analysis
    perform_pod_analysis(args.memmap_file, args.output_file, args.num_modes)