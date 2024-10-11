library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


entity PE is
	port( clk : in std_logic;
			weight_prop : in std_logic;
			weight_in : in std_logic_vector(7 downto 0);
			activation_in : in std_logic_vector(7 downto 0);
			cur_partial_sum_in : in std_logic_vector(17 downto 0);
			weight_out : out std_logic_vector(7 downto 0);
			activation_out : out std_logic_vector(7 downto 0);
			next_partial_sum_out : out std_logic_vector(17 downto 0)
			);
			
			
end PE;

architecture Behavioral of PE is

component RGSTR
	port( clk : in std_logic;
			reg_in : in std_logic_vector(17 downto 0);
			reg_out : out std_logic_vector(17 downto 0)
			);
end component;

component MULTIPLIER is	
	port ( mulT : in std_logic_vector(7 downto 0);
			 mulR : in std_logic_vector(7 downto 0);
			 result : out std_logic_vector(15 downto 0)
		   );	
end component;

component ACCUMULATOR is
	generic( size : integer := 17);
	port( summand1 : in std_logic_vector(17 downto 0);
			summand2 : in std_logic_vector(17 downto 0);
			sum : out std_logic_vector(17 downto 0)
			);
end component;

signal weight_in_reg : std_logic_vector(7 downto 0);
signal intr_weight : std_logic_vector(7 downto 0);
signal intr_activation : std_logic_vector(7 downto 0);
signal multResult : std_logic_vector(15 downto 0);
signal intr_cur_partial_sum : std_logic_vector(17 downto 0);

begin
weight_in_reg <= weight_in when (weight_prop = '1') else
					intr_weight when (weight_prop = '0') else
					(others => '0');
reg0 : RGSTR port map(clk, weight_in_reg, intr_weight);
reg1 : RGSTR port map(clk, activation_in, intr_activation);
reg2 : RGSTR port map(clk, cur_partial_sum_in, intr_cur_partial_sum);
mul : MULTIPLIER port map(intr_activation, intr_weight, multResult);
accum : ACCUMULATOR generic map(17) port map(multResult, intr_cur_partial_sum, next_partial_sum_out);
weight_out <= intr_weight;
activation_out <= intr_activation;
end Behavioral;
