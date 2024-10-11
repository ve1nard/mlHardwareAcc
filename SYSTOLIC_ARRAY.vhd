entity SYSTOLIC_ARRAY is
	generic( array_dim : integer := 4;
				word_length : integer := 8);
	
	port(	clk : in std_logic;			
			result : out std_logic_vector(array_dim * 18 - 1 downto 0)
			);
end SYSTOLIC_ARRAY;

architecture Behavioral of SYSTOLIC_ARRAY is	
	component PE is	
		port( clk : in std_logic;
				weight_prop : in std_logic;
				weight_in : in std_logic_vector(7 downto 0);
				activation_in : in std_logic_vector(7 downto 0);
				cur_partial_sum_in : in std_logic_vector(17 downto 0);
				weight_out : out std_logic_vector(7 downto 0);
				activation_out : out std_logic_vector(7 downto 0);
				next_partial_sum_out : out std_logic_vector(17 downto 0)
				);	
	end component;

	type input_array is array (integer range <>, integer range <>) of std_logic_vector(word_length - 1 downto 0);	
	
	signal weights : input_array(0 to array_dim - 1, 0 to array_dim - 1);
	signal activations : input_array(0 to array_dim - 1, array_dim - 1 downto 0);
	
	signal weights_shift : input_array(0 to array_dim - 1, 0 to array_dim - 1);
	signal activations_shift : input_array(0 to array_dim - 1, 0 to array_dim - 1);
	signal partial_sums_shift : input_array(0 to array_dim - 1, 0 to array_dim - 1);
	signal weight_prop : std_logic;	
	
begin	
	weight_propagation : process(clk)
	variable ctr : integer := 0;
	begin 
		if (rising_edge(clk)) then
			if (ctr < array_dim) then
				weight_prop <= '1';
				ctr := ctr + 1;
			else
				weight_prop <= '0';
			end if;
		end if;
	end process weight_propagation;
			
	PE00: PE port map(clk, weight_prop, weights(0,0), activations(0,0), (others => '0'), weights_shift(0,0), activations_shift(0,0), partial_sums_shift(0,0));
	
	PE_rest : for i in 1 to (array_dim - 1) generate
		PEi0 : PE port map(clk, weight_prop, weights_shift(i - 1,0), activations_shift(i - 1,0), partial_sums_shift(i - 1,0), weights_shift(i,0), activations_shift(i,0), partial_sums_shift(i,0));
		PE0i : PE port map(clk, weight_prop, weights(0,i), activations_shift(0,i - 1), (others => '0'), weights_shift(0,i), activations_shift(0,i), partial_sums_shift(0,i));
		PEJ : for j in 1 to (array_dim - 1) generate
			PEij : PE port map(clk, weight_prop, weights_shift(i - 1,j), activations_shift(i,j - 1), partial_sums_shift(i - 1,j), weights_shift(i,j), activations_shift(i,j), partial_sums_shift(i,j));
		end generate PEJ;
	end generate PE_rest;
	
	array_results : for k in array_dim downto 1 generate
		result(k * 18 - 1 downto (k - 1) * 18) <= partial_sums_shift(array_dim - 1, array_dim - k);
	end generate array_results;
end Behavioral;
