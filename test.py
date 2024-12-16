import numpy as np

import pyopencl as cl


rng = np.random.default_rng()
a_np = rng.random((25000,2500), dtype=np.float32)
b_np = rng.random((25000,2500), dtype=np.float32)

platform = cl.get_platforms()[0]
device = platform.get_devices()[0]

ctx = cl.Context([device])
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)

prg = cl.Program(ctx, """
__kernel void sum(__global const float *a_g, __global const float *b_g, __global float *res_g, const int height)
    {
    int gidx = get_global_id(0);
    int gidy = get_global_id(1);
                 
    int index = gidx + height * gidy;
    res_g[index] = a_g[index] + b_g[index];
    }
""").build()

# prg = cl.Program(ctx, """
# __kernel void sum(__global const float *a_g, __global const float *b_g, __global float *res_g)
#     {
#     int gid = get_global_id(0);
#     res_g[gid] = a_g[gid] + b_g[gid];
#     }
# """).build()

res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
knl = prg.sum  # Use this Kernel object for repeated calls
knl(queue, (a_np.shape), None, a_g, b_g, res_g, np.int32(25000))

res_np = np.empty_like(a_np)
cl.enqueue_copy(queue, res_np, res_g)

# Check on CPU with Numpy:
error_np = res_np - (a_np + b_np)
print(f"Error:\n{error_np}")
# print(f"Norm: {np.linalg.norm(error_np):.16e}")
assert np.allclose(res_np, a_np + b_np)