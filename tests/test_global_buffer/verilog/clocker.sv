module clocker
   (output logic Clk,
    output logic Reset);

   always #5 Clk <= ~Clk;
   initial begin
      Clk <= 1'b0;
      Reset <= 1'b1;//Active high reset
      repeat(20) @(posedge Clk);
      Reset <= 1'b0;
   end
endmodule


