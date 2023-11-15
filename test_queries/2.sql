SELECT nation.n_nationkey,
       nation.n_name,
       region.r_name AS region_name,
       nation.n_comment
FROM public.nation
    JOIN public.region ON nation.n_regionkey = region.r_regionkey;