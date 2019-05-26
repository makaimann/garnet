module global_buffer_tb();

logic   clk;
logic   reset;

logic [7:0]                     host_wr_strb;
logic [63:0]                    host_wr_data;
logic [31:0]                    host_wr_addr;
logic                           host_rd_en;
logic [63:0]                    host_rd_data;
logic [31:0]                    host_rd_addr;

global_buffer dut (
    .clk                    (clk),
    .reset                  (reset),

    .host_wr_strb           (host_wr_strb),
    .host_wr_addr           (host_wr_addr),
    .host_wr_data           (host_wr_data),

    .host_rd_en             (host_rd_en),
    .host_rd_addr           (host_rd_addr),
    .host_rd_data           (host_rd_data)
);

clocker clocker (.Clk(clk), .Reset(reset));


    initial begin
        $dumpfile("glb_tb.vcd");
        $dumpvars(0, global_buffer_tb);
        host_rd_en = 0;
        host_wr_strb = 0;
        host_wr_addr = 0;
        host_wr_data = 0;
        #503 $dumpall;
        host_wr_strb = 8'hFF;
        host_wr_addr = 32'h0000000F;
        host_wr_data = 64'h12345678;

        #10
        host_wr_strb = 8'h0;


        #10
        #10
        host_rd_en = 1;
        host_rd_addr = 32'h0000000F;
        #10
        host_rd_en = 0;
        #300
        $finish;
    end

endmodule
