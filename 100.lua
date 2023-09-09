repeat task.wait() until game:IsLoaded()
while wait() do
local goat = game.Players.LocalPlayer
local wendy1 = {}
local wendy2 = {}
local wendy3 = {}

for _,v in pairs(game:GetService("Workspace")._UNITS:GetChildren()) do
    if v.Name == 'wendy' and v._stats.player.Value == goat then
        table.insert(wendy1, v)
    end
end

if #wendy1 == 4 then
    while true do
        game:GetService("ReplicatedStorage"):WaitForChild("endpoints"):WaitForChild("client_to_server"):WaitForChild("use_active_attack"):InvokeServer(wendy1[1])
        wait(15.5)
        game:GetService("ReplicatedStorage"):WaitForChild("endpoints"):WaitForChild("client_to_server"):WaitForChild("use_active_attack"):InvokeServer(wendy1[3])
        wait(15.5)
        game:GetService("ReplicatedStorage"):WaitForChild("endpoints"):WaitForChild("client_to_server"):WaitForChild("use_active_attack"):InvokeServer(wendy1[2])
        wait(15.5)
        game:GetService("ReplicatedStorage"):WaitForChild("endpoints"):WaitForChild("client_to_server"):WaitForChild("use_active_attack"):InvokeServer(wendy1[4])
        wait(15.5)
    end
end
end
