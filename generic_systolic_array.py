# Word_size is the main parameter that controls the architecture
# of the systolic array
word_size = 10
temp_size_fixed = int(word_size / 2)
temp_size_i = 0
fixed_column = temp_size_fixed
triplet_i = 0
doublet_i = 0
singleton_i = 0
initial_heights = []
array_of_indices = [[]]
counter = temp_size_fixed - 2
rows_right_indents = []
indents_counter = 1
column_height_comp = 0
finish_stage_passed = False
finish_sum_passed = False
num_of_steps = 1

# This block calculates the sizes of multiply and accumulation units
# based on the word size
rows_right_indents.append(0)
rows_right_indents.append(1)
for itr in range(temp_size_fixed - 2):
   indents_counter += 2
   rows_right_indents.append(indents_counter)
initial_heights.extend([temp_size_fixed] * 6)
initial_heights.append(temp_size_fixed - 1)
initial_heights.append(temp_size_fixed - 1)
initial_heights.insert(0, temp_size_fixed - 1)
for itr in range(temp_size_fixed - 3):
   initial_heights.insert(0, counter)
   initial_heights.insert(0, counter)
   initial_heights.append(counter)
   initial_heights.append(counter)
   counter -= 1
initial_heights.insert(0, counter)
initial_heights.insert(0, counter)
initial_heights.append(counter)
for itr in range(word_size * 2):
   triplet_i = initial_heights[itr] // 3
   doublet_i = (initial_heights[itr] % 3) // 2
   singleton_i = (initial_heights[itr] % 3) % 2
   array_of_indices[0].append([triplet_i, doublet_i, singleton_i])
while (fixed_column != 2):
   array_of_indices.append([])
   for itr in range(2 * word_size):
       if itr == (2 * word_size - 1):
           temp_size_i = sum(array_of_indices[num_of_steps - 1][itr])
       else:
           temp_size_i = sum(array_of_indices[num_of_steps - 1][itr]) +\
                         array_of_indices[num_of_steps - 1][itr+1][0] +\
                         array_of_indices[num_of_steps - 1][itr+1][1]
       if itr == (word_size - 3):
           fixed_column = temp_size_i
       triplet_i = temp_size_i // 3
       doublet_i = (temp_size_i % 3) // 2
       singleton_i = (temp_size_i % 3) % 2
       if (itr == 2 * word_size - 1):
           array_of_indices[num_of_steps].append([0, 0, 1])
       elif (fixed_column == 2 and array_of_indices[num_of_steps - 1][itr + 1][0] == 0):
           if (array_of_indices[num_of_steps - 1][itr][0] == 1):
               array_of_indices[num_of_steps].append([0, 0, 1])
           elif (array_of_indices[num_of_steps - 1][itr][1] == 1):
               array_of_indices[num_of_steps].append([0, 1, 0])
           else:
               array_of_indices[num_of_steps].append([0, 0, 1])
       else:
           array_of_indices[num_of_steps].append([triplet_i, doublet_i, singleton_i])
   num_of_steps += 1
finish_stage_itr = 0
while (array_of_indices[num_of_steps - 1][2 * word_size - 1 - finish_stage_itr][2] == 1 ):
   finish_stage_itr += 1
finish_carries_size = 2 * word_size - 1 - finish_stage_itr

# This is a VHDL template code for generating a systolic array
# that is filled up by the parameters calculated above
entity_name = "MyEntity"
input_ports = ["clk", "reset"]
output_ports = ["data_out", "valid_out"]

vhdl_code_1 = f"""
library IEEE;
  use IEEE.STD_LOGIC_1164.ALL;
  use IEEE.NUMERIC_STD.ALL;
  
entity main is
  generic (
     word_size : integer := {word_size}
  );
  port (
     mulT : in std_logic_vector({word_size} - 1 downto 0);
     mulR : in std_logic_vector({word_size} - 1 downto 0);
     result : out std_logic_vector(2 * {word_size} - 1 downto 0)
  );
end main;

architecture Behavioral of main is
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
 
   signal mulR_zero : std_logic_vector({word_size} downto 0);
  type partial_products_array_type is array (0 to {temp_size_fixed - 1}) of std_logic_vector(({word_size + 2}) downto 0);
  signal partial_products_array : partial_products_array_type;
  signal last_row_carry : std_logic;
  signal temp_row1_sig : std_logic;
  signal first_stage_sums : std_logic_vector(12 downto 0);
  signal first_stage_carries : std_logic_vector(12 downto 0);
  signal final_carries : std_logic_vector(0 to {finish_carries_size - 1});
"""
vhdl_code_3 = f"""
   begin 
  first_triplet_process : process(mulT, mulR)
  variable first_triplet : std_logic_vector(2 downto 0);
  begin
     first_triplet := mulR(1 downto 0) & '0';
     case first_triplet is
        when "000"|"111" => -- 0
           partial_products_array(0)({word_size} - 1 downto 0) <= (others => '0');
           temp_row1_sig <= '0';
           partial_products_array(1)(0) <= '0';
        when "001"|"010" => -- 1
           partial_products_array(0)({word_size} - 1 downto 0) <= mulT;
           temp_row1_sig <= mulT({word_size} - 1);
           partial_products_array(1)(0) <= '0';
        when "011" => -- 2
           partial_products_array(0)({word_size} - 1 downto 1) <= mulT({word_size} - 2 downto 0);
           partial_products_array(0)(0) <= '0';
           temp_row1_sig <= mulT({word_size} - 1);
           partial_products_array(1)(0) <= '0';
        when "101"|"110" => -- -1
           partial_products_array(0)({word_size} - 1 downto 1) <= not(mulT({word_size} - 1 downto 1));
           partial_products_array(0)(0) <= mulT(0);
           temp_row1_sig <= not(mulT({word_size} - 1));
           partial_products_array(1)(0) <= not(mulT(0));
        when "100" => -- -2
           partial_products_array(0)({word_size} - 1 downto 1) <= not(mulT({word_size} - 2 downto 0));
           partial_products_array(0)(0) <= '0';
           temp_row1_sig <= not(mulT({word_size} - 1));
           partial_products_array(1)(0) <= '1';
        when others => -- 0
           partial_products_array(0)({word_size}- 1 downto 0) <= (others => '0');
           temp_row1_sig <= '0';
           partial_products_array(1)(0) <= '0';
     end case;
  end process;
"""

vhdl_code_4 = f"""
   finish_triplet_process : process(mulT, mulR)
  variable finish_triplet : std_logic_vector(2 downto 0);
  begin
     finish_triplet := mulR(({word_size} - 1) downto ({word_size} - 3));
     case finish_triplet is
        when "000"|"111" => -- 0
           partial_products_array({temp_size_fixed} - 1)(({word_size} + 2) downto ({word_size} + 1)) <= (others => '1');
           partial_products_array({temp_size_fixed} - 1)({word_size} downto 1) <= (others => '0');
           last_row_carry <= '0';
        when "001"|"010" => -- 1
           partial_products_array({temp_size_fixed} - 1)({word_size} + 2) <= '1';
           partial_products_array({temp_size_fixed} - 1)({word_size} + 1) <= not(mulT({word_size} - 1));
           partial_products_array({temp_size_fixed} - 1)({word_size} downto 1) <= mulT;
           last_row_carry <= '0';
        when "011" => -- 2
           partial_products_array({temp_size_fixed} - 1)({word_size} + 2) <= '1';
           partial_products_array({temp_size_fixed} - 1)({word_size} + 1) <= not(mulT({word_size} - 1));
           partial_products_array({temp_size_fixed} - 1)({word_size} downto 2) <= mulT(({word_size} - 2) downto 0);
           partial_products_array({temp_size_fixed} - 1)(1) <= '0';
           last_row_carry <= '0';
        when "101"|"110" => -- -1
           partial_products_array({temp_size_fixed} - 1)({word_size} + 2) <= '1';
           partial_products_array({temp_size_fixed} - 1)({word_size} + 1) <= mulT(7);
           partial_products_array({temp_size_fixed} - 1)({word_size} downto 3) <= not(mulT(({word_size} - 1) downto 2));
           partial_products_array({temp_size_fixed} - 1)(2) <= mulT(0) xor mulT(1);
           partial_products_array({temp_size_fixed} - 1)(1) <= mulT(0);
           last_row_carry <= not(mulT(0) or mulT(1));
        when "100" => -- -2
           partial_products_array({temp_size_fixed} - 1)({word_size} + 2) <= '1';
           partial_products_array({temp_size_fixed} - 1)({word_size} + 1) <= mulT(7);
           partial_products_array({temp_size_fixed} - 1)({word_size} downto 3) <= not(mulT(({word_size} - 2) downto 1));
           partial_products_array({temp_size_fixed} - 1)(2) <= mulT(0);
           partial_products_array({temp_size_fixed} - 1)(1) <= '0';
           last_row_carry <= not(mulT(0));
        when others => -- 0
           partial_products_array({temp_size_fixed} - 1)(({word_size} + 2) downto 1) <= (others => '0');
           last_row_carry <= '0';
     end case;
  end process;

   partial_products_first_row : process(mulT, mulR, temp_row1_sig, last_row_carry)
  variable temp_row1_sig_last_row_carry : std_logic_vector(1 downto 0);
  begin
     temp_row1_sig_last_row_carry := temp_row1_sig & last_row_carry;
     case temp_row1_sig_last_row_carry is
        when "00"|"11" => partial_products_array(0)(({word_size} + 2) downto {word_size}) <= "100";
        when "01" => partial_products_array(0)(({word_size} + 2) downto {word_size}) <= "101";
        when "10" => partial_products_array(0)(({word_size} + 2) downto {word_size}) <= "011";
        when others => partial_products_array(0)(({word_size} + 2) downto {word_size}) <= "000";
     end case;
  end process;
"""

# Write VHDL code to a file
with open("my_entity.vhd", "w") as file:
   file.write(vhdl_code_1)
   for itr in range(2 * word_size):
       if (initial_heights[itr] == 1):
           vhdl_code_i = \
f"""    signal stage_1_column_{itr} : std_logic;
"""
       else:
           vhdl_code_i = \
f"""    signal stage_1_column_{itr} : std_logic_vector(0 to {initial_heights[itr] - 1});
"""
       file.write(vhdl_code_i)
   for itr in range(num_of_steps - 1):
       for itr2 in range(2 * word_size):
           num_of_entries = 3 * array_of_indices[itr + 1][itr2][0] + 2 * array_of_indices[itr + 1][itr2][1] + array_of_indices[itr + 1][itr2][2]
           if (num_of_entries == 1):
               vhdl_code_i = \
f"""    signal stage_{itr + 2}_column_{itr2} : std_logic;
"""
           else:
               vhdl_code_i = \
f"""    signal stage_{itr + 2}_column_{itr2} : std_logic_vector(0 to {num_of_entries - 1});
"""
           file.write(vhdl_code_i)
   file.write(vhdl_code_3)
   for itr in range(temp_size_fixed - 2):
       vhdl_code_i = f"""
   triplet_{itr}_process : process(mulT, mulR)
  variable triplet_{itr} : std_logic_vector(2 downto 0);
  begin
     triplet_{itr} := mulR((2 * {itr} + 3) downto (2 * {itr} + 1));
     case triplet_{itr} is
        when "000"|"111" => -- 0
           partial_products_array({itr} + 1)(({word_size} + 2) downto ({word_size} + 1)) <= (others => '1');
           partial_products_array({itr} + 1)({word_size} downto 1) <= (others => '0');
           partial_products_array({itr} + 2)(0) <= '0';
        when "001"|"010" => -- 1
           partial_products_array({itr} + 1)({word_size} + 2) <= '1';
           partial_products_array({itr} + 1)({word_size} + 1) <= not(mulT({word_size} - 1));
           partial_products_array({itr} + 1)({word_size} downto 1) <= mulT;
           partial_products_array({itr} + 2)(0) <= '0';
        when "011" => -- 2
           partial_products_array({itr} + 1)({word_size} + 2) <= '1';
           partial_products_array({itr} + 1)({word_size} + 1) <= not(mulT({word_size} - 1));
           partial_products_array({itr} + 1)({word_size} downto 2) <= mulT({word_size} - 2 downto 0);
           partial_products_array({itr} + 1)(1) <= '0';
           partial_products_array({itr} + 2)(0) <= '0';
        when "101"|"110" => -- -1
           partial_products_array({itr} + 1)({word_size} + 2) <= '1';
           partial_products_array({itr} + 1)({word_size} + 1) <= mulT({word_size} - 1);
           partial_products_array({itr} + 1)({word_size} downto 2) <= not(mulT({word_size} - 1 downto 1));
           partial_products_array({itr} + 1)(1) <= mulT(0);
           partial_products_array({itr} + 2)(0) <= not(mulT(0));
        when "100" => -- -2
           partial_products_array({itr} + 1)({word_size} + 2) <= '1';
           partial_products_array({itr} + 1)({word_size} + 1) <= mulT({word_size} - 1);
           partial_products_array({itr} + 1)({word_size} downto 2) <= not(mulT({word_size} - 2 downto 0));
           partial_products_array({itr} + 1)(1) <= '0';
           partial_products_array({itr} + 2)(0) <= '1';
        when others => -- 0
           partial_products_array({itr} + 1)(({word_size} + 2) downto 1) <= (others => '0');
           partial_products_array({itr} + 2)(0) <= '0';
     end case;
  end process;
       """
       file.write(vhdl_code_i)
   file.write(vhdl_code_4)
   for itr in range(2 * word_size):
       if (itr != 0 and initial_heights[itr] < initial_heights[itr - 1]):
           column_height_comp += 1
       for itr2 in range(initial_heights[itr]):
           if (initial_heights[itr] == 1):
               vhdl_code_i = \
f"""    stage_1_column_{itr} <= partial_products_array({temp_size_fixed - 1 - itr2 - column_height_comp})({2 * word_size - 1 - rows_right_indents[temp_size_fixed - 1 - itr2 - column_height_comp] - itr});
"""
           else:
               vhdl_code_i = \
f"""    stage_1_column_{itr}({initial_heights[itr] - 1 - itr2}) <= partial_products_array({temp_size_fixed - 1 - itr2 - column_height_comp})({2 * word_size - 1 - rows_right_indents[temp_size_fixed - 1 - itr2 - column_height_comp] - itr});
"""
           file.write(vhdl_code_i)
   for itr in range(num_of_steps - 2):
       for itr2 in range(2 * word_size):
           curr_column_index = 0
           next_stage_column_index = 0
           next_stage_prev_column_index = sum(array_of_indices[itr][itr2 - 1])
           for itr3 in range(array_of_indices[itr][itr2][0]):
               vhdl_code_i = \
f"""    fa{itr}{itr2}{itr3} : full_adder port map(stage_{itr + 1}_column_{itr2}({curr_column_index}), stage_{itr + 1}_column_{itr2}({curr_column_index + 1}), stage_{itr + 1}_column_{itr2}({curr_column_index} + 2), stage_{itr + 2}_column_{itr2}({next_stage_column_index}), stage_{itr + 2}_column_{itr2 - 1}({next_stage_prev_column_index}));
"""
               file.write(vhdl_code_i)
               curr_column_index += 3
               next_stage_column_index += 1
               next_stage_prev_column_index += 1
           for itr3 in range(array_of_indices[itr][itr2][1]):
               if (itr2 == 0):
                   vhdl_code_i = \
f"""    stage_{itr + 2}_column_{itr2}({next_stage_column_index}) <= stage_{itr + 1}_column_{itr2}({curr_column_index}) xor stage_{itr + 1}_column_{itr2}({curr_column_index + 1});
"""
               else:
                   if (array_of_indices[itr + 1][itr2][0] == 0 and array_of_indices[itr + 1][itr2][1] == 0):
                       vhdl_code_i = \
f"""    ha{itr}{itr2}{itr3} : half_adder port map(stage_{itr + 1}_column_{itr2}({curr_column_index}), stage_{itr + 1}_column_{itr2}({curr_column_index + 1}), stage_{itr + 2}_column_{itr2}, stage_{itr + 2}_column_{itr2 - 1}({next_stage_prev_column_index}));
"""
                   else:
                       vhdl_code_i = \
f"""    ha{itr}{itr2}{itr3} : half_adder port map(stage_{itr + 1}_column_{itr2}({curr_column_index}), stage_{itr + 1}_column_{itr2}({curr_column_index + 1}), stage_{itr + 2}_column_{itr2}({next_stage_column_index}), stage_{itr + 2}_column_{itr2 - 1}({next_stage_prev_column_index}));
"""
               file.write(vhdl_code_i)
               curr_column_index += 2
               next_stage_column_index += 1
               next_stage_prev_column_index += 1
           for itr3 in range(array_of_indices[itr][itr2][2]):
               if ((array_of_indices[itr][itr2][0] == 0 and array_of_indices[itr][itr2][1] == 0) and (array_of_indices[itr + 1][itr2][0] == 0 and array_of_indices[itr + 1][itr2][1] == 0)):
                   vhdl_code_i = \
f"""    stage_{itr + 2}_column_{itr2} <= stage_{itr + 1}_column_{itr2};
"""
               elif (array_of_indices[itr][itr2][0] == 0 and array_of_indices[itr][itr2][1] == 0 and array_of_indices[itr + 1][itr2][1] == 1):
                   vhdl_code_i = \
f"""    stage_{itr + 2}_column_{itr2}({next_stage_column_index}) <= stage_{itr + 1}_column_{itr2};
"""
               else:
                   vhdl_code_i = \
f"""    stage_{itr + 2}_column_{itr2}({next_stage_column_index}) <= stage_{itr + 1}_column_{itr2}({curr_column_index});
"""
               file.write(vhdl_code_i)
               curr_column_index += 1
               next_stage_column_index += 1
   for itr in range(2 * word_size):
       if (array_of_indices[num_of_steps - 2][itr][0] == 1):
           finish_stage_passed = True
       if (array_of_indices[num_of_steps - 2][itr][0] == 1 and array_of_indices[num_of_steps - 2][itr + 1][1] == 1):
           vhdl_code_i = \
f"""    fa{num_of_steps - 1}{itr} : full_adder port map(stage_{num_of_steps - 1}_column_{itr}(0), stage_{num_of_steps - 1}_column_{itr}(1), stage_{num_of_steps - 1}_column_{itr}(2), stage_{num_of_steps}_column_{itr}, stage_{num_of_steps}_column_{itr - 1}(1));
"""
       elif (array_of_indices[num_of_steps - 2][itr][0] == 1):
           vhdl_code_i = \
f"""    fa{num_of_steps - 1}{itr} : full_adder port map(stage_{num_of_steps - 1}_column_{itr}(0), stage_{num_of_steps - 1}_column_{itr}(1), stage_{num_of_steps - 1}_column_{itr}(2), stage_{num_of_steps}_column_{itr}(0), stage_{num_of_steps}_column_{itr - 1}(1));
"""
       elif (array_of_indices[num_of_steps - 2][itr][1] == 1):
           if (itr == 0):
               vhdl_code_i = \
f"""    stage_{num_of_steps}_column_{itr}(0) <= stage_{num_of_steps - 1}_column_{itr}(0) xor stage_{num_of_steps - 1}_column_{itr}(1);
"""
           elif (not finish_stage_passed):
               vhdl_code_i = \
f"""    ha{num_of_steps - 1}{itr} : half_adder port map(stage_{num_of_steps - 1}_column_{itr}(0), stage_{num_of_steps - 1}_column_{itr}(1), stage_{num_of_steps}_column_{itr}(0), stage_{num_of_steps}_column_{itr - 1}(1));
"""
           else:
               vhdl_code_i = \
f"""    stage_{num_of_steps}_column_{itr}(0) <= stage_{num_of_steps - 1}_column_{itr}(0);
       stage_{num_of_steps}_column_{itr}(1) <= stage_{num_of_steps - 1}_column_{itr}(1);
"""
       elif (array_of_indices[num_of_steps - 2][itr][2] == 1):
           if (array_of_indices[num_of_steps - 1][itr][1] == 1):
               vhdl_code_i = \
f"""    stage_{num_of_steps}_column_{itr}(0) <= stage_{num_of_steps - 1}_column_{itr};
"""
           elif (array_of_indices[num_of_steps - 1][itr][2] == 1):
               vhdl_code_i = \
f"""    stage_{num_of_steps}_column_{itr} <= stage_{num_of_steps - 1}_column_{itr};
"""
       file.write(vhdl_code_i)

   for itr in range(2 * word_size - 1):
       if ((array_of_indices[num_of_steps - 1][2 * word_size - 1 - itr][2] == 1) and (not finish_sum_passed) ):
           vhdl_code_i = \
f"""    result({itr}) <= stage_{num_of_steps}_column_{2 * word_size - 1 - itr};
"""
       elif ((array_of_indices[num_of_steps - 1][2 * word_size - 1 - itr][1] == 1) and (not finish_sum_passed)):
           finish_sum_passed = True
           vhdl_code_i = \
f"""    ha{num_of_steps}{itr} : half_adder port map(stage_{num_of_steps}_column_{2 * word_size - 1 - itr}(0), stage_{num_of_steps}_column_{2 * word_size - 1 - itr}(1), result({itr}), final_carries({itr - finish_stage_itr}));
"""
       elif ((array_of_indices[num_of_steps - 1][2 * word_size - 1 - itr][2] == 1) and finish_sum_passed):
           vhdl_code_i = \
f"""    ha{num_of_steps}{itr} : half_adder port map(stage_{num_of_steps}_column_{2 * word_size - 1 - itr}, final_carries({itr - finish_stage_itr - 1}), result({itr}), final_carries({itr - finish_stage_itr}));
"""
       else:
           vhdl_code_i = \
f"""    fa{num_of_steps}{itr} : full_adder port map(stage_{num_of_steps}_column_{2 * word_size - 1 - itr}(0), stage_{num_of_steps}_column_{2 * word_size - 1 - itr}(1), final_carries({itr - finish_stage_itr - 1}), result({itr}), final_carries({itr - finish_stage_itr}));
"""
       file.write(vhdl_code_i)
   vhdl_code_final = \
f"""    result({2 * word_size - 1}) <= stage_{num_of_steps}_column_0(0) xor stage_{num_of_steps}_column_0(1) xor final_carries({finish_carries_size - 1});
   end Behavioral;
"""
   file.write(vhdl_code_final)

