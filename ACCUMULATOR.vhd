entity ACCUMULATOR is
	generic( size : integer := 17);
	port( summand1 : in std_logic_vector(17 downto 0);
			summand2 : in std_logic_vector(17 downto 0);
			sum : out std_logic_vector(17 downto 0)
			);
end ACCUMULATOR;

architecture Behavioral of ACCUMULATOR is
component full_adder is
	port ( a : in  std_logic;
			 b : in  std_logic;
			 c : in  std_logic;
			 sum : out  std_logic;
			 carry : out  std_logic
			);
end component;

component half_adder is
	port ( a : in  std_logic;
			 b : in  std_logic;
			 sum : out  std_logic;
			 carry : out  std_logic
			);
end component;

signal carries : std_logic_vector(size - 1 downto 0); 
begin
sum_generation : for itr in 0 to size generate
	bit1 : if (itr = 0) generate
		ha : half_adder port map(summand1(itr), summand2(itr), sum(itr), carries(itr));
	end generate bit1;
	fa : full_adder port map(summand1(itr), summand2(itr), carries(itr - 1), sum(itr), carries(itr));	
end generate sum_generation;

end Behavioral;

