library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity RGSTR is
	port( clk : in std_logic;
			reg_in : in std_logic_vector(17 downto 0);
			reg_out : out std_logic_vector(17 downto 0)
			);
end RGSTR;

architecture Behavioral of RGSTR is

begin
reg : process(clk)
	begin
		if(rising_edge(clk)) then
			reg_out <= reg_in;
		end if;
end process reg;
end Behavioral;
