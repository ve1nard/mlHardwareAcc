library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
USE ieee.std_logic_signed.ALL;

entity booth_multiplier is

	generic ( termSize : integer := 4);
	port ( mt : in std_logic_vector(termSize - 1 downto 0);
			 mr : in std_logic_vector(termSize - 1 downto 0);
			 result : out std_logic_vector(2*termSize - 1 downto 0));
			
			

end booth_multiplier;

architecture Behavioral of booth_multiplier is


begin

		process(mt, mr)
		
		constant zeros : std_logic_vector(termSize - 1 downto 0) :=  (others => '0');
		constant resultSize : integer := 2 * termSize;
		variable mtComp : std_logic_vector(termSize - 1 downto 0);
		variable accMr : std_logic_vector(resultSize downto 0) := (others => '0');
		variable temp : std_logic_vector(termSize - 1 downto 0);
		
		begin
			
			accMr(resultSize downto termSize + 1) := (others => '0');
			accMr(termSize downto 1) := mr;
			accMr(0) := '0';
			
			
			if (mt /= zeros and mr /= zeros)then
			
				for iter in 1 to termSize loop
				
					temp := accMr(resultSize downto termSize + 1);
					mtComp := not (mt) + 1;
					if (accMr(1 downto 0) = "10") then
						temp := temp + mtComp;
					elsif (accMr(1 downto 0) = "01") then
						temp := temp + mt;
					end if;
					accMr(resultSize downto termSize + 1) := temp;
					accMr(resultSize - 1 downto 0) := accMr(resultSize downto 1);					
					
				end loop;	
				
			end if;
			
			result <= accMr(resultSize downto 1);
		
		end process;

end Behavioral;



