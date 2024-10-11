library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity MULTIPLIER is
	
	port ( mulT : in std_logic_vector(7 downto 0);
			 mulR : in std_logic_vector(7 downto 0);
			 result : out std_logic_vector(17 downto 0)
		   );
	
end MULTIPLIER;

architecture Behavioral of MULTIPLIER is

	component full_adder is
		 Port ( a : in  std_logic;
				  b : in  std_logic;
				  c : in  std_logic;
				  sum : out  std_logic;
				  carry : out  std_logic);
	end component;

	component half_adder is
		 Port ( a : in  std_logic;
				  b : in  std_logic;
				  sum : out  std_logic;
				  carry : out  std_logic);
	end component;
	
	signal mulR_with_zero : std_logic_vector(8 downto 0);
	signal triplet_first : std_logic_vector(2 downto 0);
	signal triplet_second : std_logic_vector(2 downto 0);
	signal triplet_third : std_logic_vector(2 downto 0);
	signal triplet_fourth : std_logic_vector(2 downto 0);
	type partial_products_array_type is array (0 to 3) of std_logic_vector(8 downto 0);
	signal partial_products_array : partial_products_array_type;
	signal sums_stage_one : std_logic_vector(0 to 11);
	signal sums_stage_two : std_logic_vector(0 to 6);
	signal sums_stage_three : std_logic_vector(0 to 7);
	signal carry_stage_one : std_logic_vector(0 to 11);
	signal carry_stage_two : std_logic_vector(0 to 6);
	signal carry_stage_three : std_logic_vector(0 to 7);
	signal twos_complement_carries : std_logic_vector(0 to 3);
	signal carry_final : std_logic_vector(0 to 14);
	signal bit15 : std_logic;

begin

	mulR_with_zero(8 downto 1) <= mulR;
	mulR_with_zero(0) <= '0';	
	
	triplet_first <= mulR_with_zero(2) & mulR_with_zero(1) & mulR_with_zero(0); 
	process (mulT, mulR_with_zero, triplet_first)
	begin
		case triplet_first is
				
			when "000" | "111" => -- 0
				partial_products_array(0)(7 downto 0) <= (others => '0');
				partial_products_array(0)(8) <= '1';
				twos_complement_carries(0) <= '0';					
					
			when "001" | "010" => -- 1
				partial_products_array(0)(7 downto 0) <= mulT;
				partial_products_array(0)(8) <= not mulT(7);
				twos_complement_carries(0) <= '0';
						
			when "101" | "110" => -- -1
				partial_products_array(0)(7 downto 0) <= not mulT;
				partial_products_array(0)(8) <= mulT(7);
				twos_complement_carries(0) <= '1';
						
			when "011" => -- 2
				partial_products_array(0)(7 downto 1) <= mulT(6 downto 0); 
				partial_products_array(0)(0) <= '0';
				partial_products_array(0)(8) <= not mulT(7);
				twos_complement_carries(0) <= '0';
						
			when "100" => -- -2
				partial_products_array(0)(7 downto 1) <= not mulT(6 downto 0); 
				partial_products_array(0)(0) <= '1';		
				partial_products_array(0)(8) <= mulT(7);
				twos_complement_carries(0) <= '1';
					
			when others => -- other cases
				partial_products_array(0) <= (others => '0');
				twos_complement_carries(0) <= '0';
				
		end case;
		
	end process;

	triplet_second <= mulR_with_zero(4) & mulR_with_zero(3) & mulR_with_zero(2); 
	process(mulT, mulR_with_zero, triplet_second)
	begin
		case triplet_second is
				
			when "000" | "111" => -- 0
				partial_products_array(1)(7 downto 0) <= (others => '0');
				partial_products_array(1)(8) <= '1';
				twos_complement_carries(1) <= '0';					
					
			when "001" | "010" => -- 1
				partial_products_array(1)(7 downto 0) <= mulT;
				partial_products_array(1)(8) <= not mulT(7);
				twos_complement_carries(1) <= '0';
						
			when "101" | "110" => -- -1
				partial_products_array(1)(7 downto 0) <= not mulT;
				partial_products_array(1)(8) <= mulT(7);
				twos_complement_carries(1) <= '1';
						
			when "011" => -- 2
				partial_products_array(1)(7 downto 1) <= mulT(6 downto 0); 
				partial_products_array(1)(0) <= '0';
				partial_products_array(1)(8) <= not mulT(7);
				twos_complement_carries(1) <= '0';
						
			when "100" => -- -2
				partial_products_array(1)(7 downto 1) <= not mulT(6 downto 0); 
				partial_products_array(1)(0) <= '1';
				partial_products_array(1)(8) <= mulT(7);
				twos_complement_carries(1) <= '1';
					
			when others => -- other cases
				partial_products_array(1) <= (others => '0');
				twos_complement_carries(1) <= '0';
				
		end case;
	end process;
	
	triplet_third <= mulR_with_zero(6) & mulR_with_zero(5) & mulR_with_zero(4); 
	process(mulT, mulR_with_zero, triplet_third)
	begin
		case triplet_third is
				
			when "000" | "111" => -- 0
				partial_products_array(2)(7 downto 0) <= (others => '0');
				partial_products_array(2)(8) <= '1';
				twos_complement_carries(2) <= '0';					
					
			when "001" | "010" => -- 1
				partial_products_array(2)(7 downto 0) <= mulT;
				partial_products_array(2)(8) <= not mulT(7);
				twos_complement_carries(2) <= '0';
						
			when "101" | "110" => -- -1
				partial_products_array(2)(7 downto 0) <= not mulT;
				partial_products_array(2)(8) <= mulT(7);
				twos_complement_carries(2) <= '1';
						
			when "011" => -- 2
				partial_products_array(2)(7 downto 1) <= mulT(6 downto 0); 
				partial_products_array(2)(0) <= '0';
				partial_products_array(2)(8) <= not mulT(7);
				twos_complement_carries(2) <= '0';
						
			when "100" => -- -2
				partial_products_array(2)(7 downto 1) <= not mulT(6 downto 0); 
				partial_products_array(2)(0) <= '1';
				partial_products_array(2)(8) <= mulT(7);
				twos_complement_carries(2) <= '1';
					
			when others => -- other cases
				partial_products_array(2) <= (others => '0');
				twos_complement_carries(2) <= '0';
				
		end case;
	end process;
	
	triplet_fourth <= mulR_with_zero(8) & mulR_with_zero(7) & mulR_with_zero(6); 
	process(mulT, mulR_with_zero, triplet_fourth)
	begin
		case triplet_fourth is
				
			when "000" | "111" => -- 0
				partial_products_array(3)(7 downto 0) <= (others => '0');
				partial_products_array(3)(8) <= '0';
				twos_complement_carries(3) <= '0';					
					
			when "001" | "010" => -- 1
				partial_products_array(3)(7 downto 0) <= mulT;
				partial_products_array(3)(8) <= mulT(7);
				twos_complement_carries(3) <= '0';
						
			when "101" | "110" => -- -1
				partial_products_array(3)(7 downto 0) <= not mulT;
				partial_products_array(3)(8) <= not mulT(7);
				twos_complement_carries(3) <= '1';
						
			when "011" => -- 2
				partial_products_array(3)(7 downto 1) <= mulT(6 downto 0); 
				partial_products_array(3)(0) <= '0';
				partial_products_array(3)(8) <= mulT(7);
				twos_complement_carries(3) <= '0';
						
			when "100" => -- -2
				partial_products_array(3)(7 downto 1) <= not mulT(6 downto 0); 
				partial_products_array(3)(0) <= '1';
				partial_products_array(3)(8) <= not mulT(7);
				twos_complement_carries(3) <= '1';
					
			when others => -- other cases
				partial_products_array(3) <= (others => '0');
				twos_complement_carries(3) <= '0';
				
		end case;
		
	end process;
	
	-- Stage one

	fa00 : full_adder port map(partial_products_array(0)(2), partial_products_array(1)(0), twos_complement_carries(1), sums_stage_one(0), carry_stage_one(0));
	ha00 : half_adder port map(partial_products_array(0)(3), partial_products_array(1)(1), sums_stage_one(1), carry_stage_one(1));
	fa01 : full_adder port map(partial_products_array(0)(4), partial_products_array(1)(2), partial_products_array(2)(0), sums_stage_one(2), carry_stage_one(2));
	fa02 : full_adder port map(partial_products_array(0)(5), partial_products_array(1)(3), partial_products_array(2)(1), sums_stage_one(3), carry_stage_one(3));
	fa03 : full_adder port map(partial_products_array(0)(6), partial_products_array(1)(4), partial_products_array(2)(2), sums_stage_one(4), carry_stage_one(4));
	ha01 : half_adder port map(partial_products_array(3)(0), twos_complement_carries(3), sums_stage_one(5), carry_stage_one(5));
	fa04 : full_adder port map(partial_products_array(0)(7), partial_products_array(1)(5), partial_products_array(2)(3), sums_stage_one(6), carry_stage_one(6));
	fa05 : full_adder port map(partial_products_array(0)(8), partial_products_array(1)(6), partial_products_array(2)(4), sums_stage_one(7), carry_stage_one(7));	
	ha02 : half_adder port map(partial_products_array(3)(2), '1', sums_stage_one(8), carry_stage_one(8));
	fa06 : full_adder port map(partial_products_array(1)(7), partial_products_array(2)(5), partial_products_array(3)(3), sums_stage_one(9), carry_stage_one(9));
	fa07 : full_adder port map(partial_products_array(1)(8), partial_products_array(2)(6), partial_products_array(3)(4), sums_stage_one(10), carry_stage_one(10));	
	fa08 : full_adder port map(partial_products_array(2)(7), partial_products_array(3)(5), '1', sums_stage_one(11), carry_stage_one(11));	
	
	-- Stage two
	
	fa10 : full_adder port map(sums_stage_one(2), twos_complement_carries(2), carry_stage_one(1), sums_stage_two(0), carry_stage_two(0));
	ha10 : half_adder port map(sums_stage_one(3), carry_stage_one(2), sums_stage_two(1), carry_stage_two(1));
	fa11 : full_adder port map(sums_stage_one(4), sums_stage_one(5), carry_stage_one(3), sums_stage_two(2), carry_stage_two(2));	
	fa12 : full_adder port map(sums_stage_one(6),partial_products_array(3)(1), carry_stage_one(4), sums_stage_two(3), carry_stage_two(3));
	fa13 : full_adder port map(sums_stage_one(7), sums_stage_one(8), carry_stage_one(6), sums_stage_two(4), carry_stage_two(4));
	fa14 : full_adder port map(sums_stage_one(9), '1', carry_stage_one(7), sums_stage_two(5), carry_stage_two(5));
	ha11 : half_adder port map(sums_stage_one(10), carry_stage_one(9), sums_stage_two(6), carry_stage_two(6));
	
	-- Stage three
	
	fa20 : full_adder port map(sums_stage_two(3), carry_stage_one(5), carry_stage_two(2), sums_stage_three(0), carry_stage_three(0));
	ha20 : half_adder port map(sums_stage_two(4), carry_stage_two(3), sums_stage_three(1), carry_stage_three(1)); 
	fa21 : full_adder port map(sums_stage_two(5), carry_stage_one(8), carry_stage_two(4), sums_stage_three(2), carry_stage_three(2));
	ha21 : half_adder port map(sums_stage_two(6), carry_stage_two(5), sums_stage_three(3), carry_stage_three(3));
	fa22 : full_adder port map(sums_stage_one(11), carry_stage_one(10), carry_stage_two(6), sums_stage_three(4), carry_stage_three(4));
	ha22 : half_adder port map(partial_products_array(2)(8), partial_products_array(3)(6), sums_stage_three(5), carry_stage_three(5));
	ha23 : half_adder port map(partial_products_array(3)(7), '1', sums_stage_three(6), carry_stage_three(6));
	ha24 : half_adder port map(partial_products_array(3)(8), '1', sums_stage_three(7), carry_stage_three(7));
	
	-- Final addition
	
	ha30 : half_adder port map(partial_products_array(0)(0), twos_complement_carries(0), result(0), carry_final(0));
	ha31 : half_adder port map(partial_products_array(0)(1), carry_final(0), result(1), carry_final(1));
	ha32 : half_adder port map(sums_stage_one(0), carry_final(1), result(2), carry_final(2));
	fa30 : full_adder port map(sums_stage_one(1), carry_stage_one(0), carry_final(2), result(3), carry_final(3));
	ha33 : half_adder port map(sums_stage_two(0), carry_final(3), result(4), carry_final(4));
	fa31 : full_adder port map(sums_stage_two(1), carry_stage_two(0), carry_final(4), result(5), carry_final(5));
	fa32 : full_adder port map(sums_stage_two(2), carry_stage_two(1), carry_final(5), result(6), carry_final(6));
	ha34 : half_adder port map(sums_stage_three(0), carry_final(6), result(7), carry_final(7));
	fa33 : full_adder port map(sums_stage_three(1), carry_stage_three(0), carry_final(7), result(8), carry_final(8));
	fa34 : full_adder port map(sums_stage_three(2), carry_stage_three(1), carry_final(8), result(9), carry_final(9));
	fa35 : full_adder port map(sums_stage_three(3), carry_stage_three(2), carry_final(9), result(10), carry_final(10));
	fa36 : full_adder port map(sums_stage_three(4), carry_stage_three(3), carry_final(10), result(11), carry_final(11));
	fa37 : full_adder port map(sums_stage_three(5), carry_stage_three(4), carry_final(11), result(12), carry_final(12));
	fa38 : full_adder port map(sums_stage_three(6), carry_stage_three(5), carry_final(12), result(13), carry_final(13));
	fa39 : full_adder port map(sums_stage_three(7), carry_stage_three(6), carry_final(13), result(14), carry_final(14));
	--result(15) <= '1' xor carry_stage_three(7) xor carry_final(14); 	
	bit15 <= not (carry_stage_three(7) xor carry_final(14));
	result(15) <= bit15;
	result(16) <= bit15;
	result(17) <= bit15;

end Behavioral;
